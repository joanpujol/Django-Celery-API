from celery import shared_task
from django.template import Template, Context
from testcartloop import celery

from . import models
from . import scheduler


@shared_task(name=celery.DISPATCH_CHATS_TASK)
def dispatch_chats():
    def render_payload(payload, operator, client, discount):
        """Renders {{ operator.full_name }}, {{ client.first_name }} and {{ discount.discount_code }}"""
        template = Template(payload)
        context = Context({
            'operator': operator,
            'client': client,
            'discount': discount,
        })
        return template.render(context)
    chats = scheduler.ChatScheduler().retrieve_current_timeslot_chats()
    for chat in chats:
        chat.payload = render_payload(chat.payload, chat.conversation.operator, chat.conversation.client, chat.discount)
        # This is where we could send this message via email/SMS
        chat.status = models.Chat.ChatStatusChoices.SENT
        chat.save()
