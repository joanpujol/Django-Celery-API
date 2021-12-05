from celery import shared_task
from django.template import Template, Context
from testcartloop import celery

from . import models


@shared_task(name=celery.DISPATCH_CHATS_TASK)
def dispatch_chats(chats):
    def render_payload(payload, operator, client, discount):
        """Renders {{ operator.full_name }}, {{ client.first_name }} and {{ discount.discount_code }}"""
        template = Template(payload)
        context = Context({
            'operator': operator,
            'client': client,
            'discount': discount,
        })
        return template.render(context)

    for chat in chats:
        chat.payload = render_payload(chat.payload, chat.conversation.operator, chat.conversation.client, chat.discount)
        # This is where we could send this message via email/SMS
        chat.status = models.ChatStatusChoices.SENT
        chat.save()
