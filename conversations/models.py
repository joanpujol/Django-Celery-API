from django.db import models

import pytz

from . import validators


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


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
