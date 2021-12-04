from django.db import models

import pytz

from . import validators


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class ConversationStatusChoices(models.IntegerChoices):
    PENDING = 1
    RESOLVED = 2


class Store(models.Model):
    name = models.CharField(max_length=20)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    phone = models.CharField(validators=[validators.phone_regex], max_length=60)


class Client(models.Model):
    user = models.CharField(max_length=20)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    phone = models.CharField(validators=[validators.phone_regex], max_length=60)


class OperatorGroup(models.Model):
    name = models.CharField(max_length=20)


class Operator(models.Model):
    user = models.CharField(max_length=20)
    operator_group = models.ForeignKey(OperatorGroup, on_delete=models.CASCADE)


class Discount(models.Model):
    discount_code = models.CharField(max_length=20)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class Conversation(models.Model):
    status = models.CharField(max_length=32, choices=ConversationStatusChoices.choices, default='UTC')
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
