from datetime import datetime
from datetime import timedelta

import pytz
from testcartloop import settings

from . import models


class ChatScheduler:
    MAX_MESSAGES_PER_HOUR = settings.MAX_MESSAGES_PER_HOUR
    SENDING_INTERVAL_START = settings.SENDING_INTERVAL_START
    SENDING_INTERVAL_END = settings.SENDING_INTERVAL_END

    def __init__(self, chat_instance):
        self.chat = chat_instance
        current_conversation = self.chat.conversation
        user = current_conversation.user
        store = current_conversation.store
        self.user_tz = user.timezone
        self.store_tz = store.timezone
        self.current_utc_dt = datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=pytz.utc)

    def schedule_dispatch(self):
        """Searches an available timeslot within the user or store tz and creates a Schedule entry in the db"""
        available_timeslot = self._search_timeslot()
        models.Schedule.objects.create(sending_date=available_timeslot, chat=self.chat)

    def _search_timeslot(self):
        start_hour = self.current_utc_dt
        end_hour = start_hour + timedelta(hours=1)
        messages_per_hour = max_messages_per_hour = self.MAX_MESSAGES_PER_HOUR
        while messages_per_hour >= max_messages_per_hour:
            if self._is_within_sending_interval(start_hour):
                messages_per_hour = models.Schedule.objects.count(
                    sending_date__gte=start_hour,
                    sending_date__lte=end_hour
                )
            if messages_per_hour < max_messages_per_hour:
                break
            start_hour += timedelta(hours=1)
            end_hour += timedelta(hours=1)
        return start_hour

    def _is_within_sending_interval(self, dt):
        reference_tz = self.user_tz or self.store_tz
        tz = pytz.timezone(reference_tz)
        datetime_in_timezone = self._get_datetime_in_timezone(dt, tz)
        return self.SENDING_INTERVAL_START <= datetime_in_timezone.hour <= self.SENDING_INTERVAL_END

    @staticmethod
    def _get_datetime_in_timezone(dt, tz):
        if dt.tzinfo is None:  # Makes datetime tz aware if it's naive
            dt = dt.replace(tzinfo=pytz.utc)
        return dt.astimezone(pytz.timezone(tz))
