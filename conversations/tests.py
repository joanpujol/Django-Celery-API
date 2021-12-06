from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status as request_status

from . import models


class ConversationsAPITestCase(APITestCase):
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
            'payload': "This is a test message sent by the user {{ client.user.first_name }}",
            'discount': self.test_discount.id,
            'conversation': self.test_conversation.id
        }
        response = self.client.post(reverse('chats'), data)
        self.assertEqual(response.status_code, request_status.HTTP_201_CREATED)

    def test_chats_list(self):
        response = self.client.get(reverse('chats'))
        self.assertEqual(response.status_code, request_status.HTTP_200_OK)
