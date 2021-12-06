import logging

from celery import shared_task
from django import template as django_template
from testcartloop import celery

from . import models
from . import scheduler


@shared_task(name=celery.DISPATCH_CHATS_TASK)
def dispatch_chats():
    def render_payload(payload, operator, client, discount):
        """Renders {{ operator.full_name }}, {{ client.first_name }} and {{ discount.discount_code }}"""
        template = django_template.Template(payload)
        context = django_template.Context({
            'operator': operator,
            'client': client,
            'discount': discount,
        })
        return template.render(context)
    chats = scheduler.ChatScheduler().retrieve_current_timeslot_chats()
    for chat in chats:
        rendered_payload = render_payload(
            payload=chat.payload,
            operator=chat.conversation.operator,
            client=chat.conversation.client,
            discount=chat.discount
        )
        # This is where we could send this payload via email/SMS
        logging.info(rendered_payload)
        chat.status = models.Chat.ChatStatusChoices.SENT
        chat.save()
