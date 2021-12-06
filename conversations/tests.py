from datetime import datetime
from datetime import timedelta

import pytz
from django.test import Client
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status as request_status
from unittest.mock import MagicMock

from . import models
from . import scheduler


class TestBase:
    def setUp(self):
        password = "Password123"
        phone = "123456789"
        self.test_user = models.User.objects.create_user(username="test_user", password=password)
        self.test_operator_user = models.User.objects.create_user(username="test_operator", password=password)
        self.test_store = models.Store.objects.create(name="test_store", phone=phone)
        self.test_client = models.Client.objects.create(user=self.test_user, phone=phone)
        self.test_operator_group = models.OperatorGroup.objects.create(name="test_operator_group")
        self.test_operator = models.Operator.objects.create(
            user=self.test_operator_user,
            operator_group=self.test_operator_group
        )
        self.test_discount = models.Discount.objects.create(store=self.test_store, discount_code="TEST_DISCOUNT")
        self.test_conversation = models.Conversation.objects.create(
            status=models.Conversation.ConversationStatusChoices.PENDING,
            store=self.test_store,
            client=self.test_client,
            operator=self.test_operator
        )


class ConversationsAPITestCase(TestBase, APITestCase):
    def test_conversations_post(self):
        data = {
            'status': models.Conversation.ConversationStatusChoices.PENDING,
            'store': self.test_store.id,
            'client': self.test_client.id,
            'operator': self.test_operator.id
        }
        response = self.client.post(reverse('conversations'), data)
        self.assertEqual(response.status_code, request_status.HTTP_201_CREATED)

    def test_conversations_list(self):
        response = self.client.get(reverse('conversations'))
        self.assertEqual(response.status_code, request_status.HTTP_200_OK)

    def test_chats_post(self):
        data = {
            'status': 1,
            'payload': 'This is a test message sent by the user {{ client.user.first_name }}',
            'discount': self.test_discount.id,
            'conversation': self.test_conversation.id
        }
        response = self.client.post(reverse('chats'), data)
        self.assertEqual(response.status_code, request_status.HTTP_201_CREATED)

    def test_chats_list(self):
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, request_status.HTTP_200_OK)


class ChatSchedulerTestCase(TestBase, TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.scheduler = scheduler.ChatScheduler()
        self.test_chat = models.Chat.objects.create(
            status=models.Chat.ChatStatusChoices.NEW,
            payload='This is a test message sent by the user {{ client.user.first_name }}',
            discount=self.test_discount,
            conversation=self.test_conversation
        )
        self.test_schedule = models.Schedule.objects.create(
            sending_date=datetime.utcnow().replace(minute=0, second=0, microsecond=0, tzinfo=pytz.utc),
            chat=self.test_chat
        )

    def test_datetime_in_timezone(self):
        current_utc_dt = self.scheduler.current_utc_dt
        current_est_dt = self.scheduler._get_datetime_in_timezone(current_utc_dt, 'EST')
        self.assertEqual(
            current_utc_dt.strftime('%y-%m-%d %a %H'), (current_est_dt + timedelta(hours=5)).strftime('%y-%m-%d %a %H')
        )

    def test_is_within_sending_interval(self):
        dt = datetime(year=2015, month=2, day=1, hour=10)
        self.scheduler._get_datetime_in_timezone = MagicMock(return_value=datetime(year=2015, month=2, day=1, hour=15))
        is_within_sending_interval = self.scheduler._is_within_sending_interval(dt, 'example-tz', 'example-tz')
        self.assertTrue(is_within_sending_interval)

    def test_search_available_timeslot(self):
        # TODO This test could be improved by testing that the next hour is filled up
        self.scheduler._is_within_sending_interval = MagicMock(return_value=True)
        available_timeslot = self.scheduler._search_available_timeslot('example-tz', 'example-tz')
        next_hour = self.scheduler.current_utc_dt + timedelta(hours=1)
        self.assertEqual(next_hour, available_timeslot)

    def test_retrieve_current_timeslot_chats(self):
        chats = self.scheduler.retrieve_current_timeslot_chats()
        self.assertEqual(chats[0], self.test_chat)
