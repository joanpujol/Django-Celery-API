from datetime import datetime
from datetime import timedelta

import pytz
from testcartloop import settings

from . import models


class ChatScheduler:
    MAX_MESSAGES_PER_HOUR = settings.MAX_MESSAGES_PER_HOUR
    SENDING_INTERVAL_START = settings.SENDING_INTERVAL_START
    SENDING_INTERVAL_END = settings.SENDING_INTERVAL_END

    def __init__(self):
        self.current_utc_dt = datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=pytz.utc)

    def schedule_dispatch(self, chat_instance):
        """Searches an available timeslot within the user or store tz and creates a Schedule entry in the db"""
        current_conversation = chat_instance.conversation
        user_tz = current_conversation.client.timezone
        store_tz = current_conversation.store.timezone
        available_timeslot = self._search_available_timeslot(user_tz, store_tz)
        models.Schedule.objects.create(sending_date=available_timeslot, chat=chat_instance)

    def retrieve_current_timeslot_chats(self):
        """Retrieves current pending chats"""
        return models.Schedule.objects.filter(
            sending_date__gte=self.current_utc_dt,
            sending_date__lte=self.current_utc_dt + timedelta(hours=1)
        ).only("chat")

    def _search_available_timeslot(self, client_tz, store_tz):
        """Looks for an hour with fewer messages than the limit and within min/max user or store interval"""
        start_hour = self.current_utc_dt + timedelta(hours=1)  # Next scheduler call will be in at least an hour
        end_hour = start_hour + timedelta(hours=1)
        messages_per_hour = max_messages_per_hour = self.MAX_MESSAGES_PER_HOUR
        while messages_per_hour >= max_messages_per_hour:
            if self._is_within_sending_interval(start_hour, client_tz, store_tz):
                messages_per_hour = models.Schedule.objects.filter(
                    sending_date__gte=start_hour,
                    sending_date__lt=end_hour
                ).count()
            if messages_per_hour < max_messages_per_hour:
                break
            start_hour += timedelta(hours=1)
            end_hour += timedelta(hours=1)
        return start_hour

    def _is_within_sending_interval(self, dt, client_tz, store_tz):
        reference_tz = client_tz or store_tz
        datetime_in_timezone = self._get_datetime_in_timezone(dt, reference_tz)
        return self.SENDING_INTERVAL_START <= datetime_in_timezone.hour <= self.SENDING_INTERVAL_END

    @staticmethod
    def _get_datetime_in_timezone(dt, tz):
        if dt.tzinfo is None:  # Makes datetime tz aware if it's naive
            dt = dt.replace(tzinfo=pytz.utc)
        return dt.astimezone(pytz.timezone(tz))
