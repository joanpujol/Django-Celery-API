from django.contrib import admin

from . import models


admin.site.register(models.Store)
admin.site.register(models.Client)
admin.site.register(models.OperatorGroup)
admin.site.register(models.Operator)
admin.site.register(models.Discount)
admin.site.register(models.Conversation)
admin.site.register(models.Chat)
admin.site.register(models.Schedule)
