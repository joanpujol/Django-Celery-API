from django.db import models

import pytz

from . import validators


class Store(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    name = models.CharField(max_length=20)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    phone = models.CharField(validators=[validators.phone_regex], max_length=60)
