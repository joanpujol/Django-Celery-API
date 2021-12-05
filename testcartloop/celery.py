import os

from celery import Celery
from celery import schedules

DISPATCH_CHATS_TASK = "DISPATCH_CHATS_TASK"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcartloop.settings')

app = Celery('testcartloop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'dispatch-chats-every-hour': {
        'task': DISPATCH_CHATS_TASK,
        'schedule': schedules.crontab(minute=0, hour='*'),
    },
}
app.conf.timezone = 'UTC'

app.autodiscover_tasks()
