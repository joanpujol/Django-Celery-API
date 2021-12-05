from django.db import models
import pytz

from . import scheduler
from . import validators


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Store(models.Model):
    name = models.CharField(max_length=20)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    phone = models.CharField(validators=[validators.phone_validation], max_length=60)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.CharField(max_length=20)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    phone = models.CharField(max_length=60, validators=[validators.phone_validation])

    def __str__(self):
        return self.user


class OperatorGroup(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Operator(models.Model):
    user = models.CharField(max_length=20)
    operator_group = models.ForeignKey(OperatorGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Discount(models.Model):
    discount_code = models.CharField(max_length=20)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store} | {self.discount_code}"


class Conversation(models.Model):
    class ConversationStatusChoices(models.IntegerChoices):
        PENDING = 1, 'Pending'
        RESOLVED = 2, 'Resolved'

    status = models.IntegerField(choices=ConversationStatusChoices.choices, default=ConversationStatusChoices.PENDING)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store} | {self.operator} => {self.client} | {self.get_status_display()}"


class ChatManager(models.Manager):
    def create(self, *args, **kwargs):
        instance = super(ChatManager, self).create(*args, **kwargs)
        scheduler.ChatScheduler().schedule_dispatch(instance)
        return instance


class Chat(models.Model):
    class ChatStatusChoices(models.IntegerChoices):
        NEW = 1, 'New'
        SENT = 2, 'Sent'

    objects = ChatManager()
    status = models.IntegerField(choices=ChatStatusChoices.choices, default=ChatStatusChoices.NEW)
    payload = models.CharField(max_length=300, validators=[validators.chat_validation])
    created_date = models.DateTimeField(auto_now_add=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.payload} | {self.get_status_display()}"


class Schedule(models.Model):
    sending_date = models.DateTimeField()
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sending_date} => {self.chat}"
