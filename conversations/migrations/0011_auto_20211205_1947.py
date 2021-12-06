# Generated by Django 3.2.9 on 2021-12-05 19:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0010_alter_chat_conversation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='payload',
            field=models.CharField(max_length=300, validators=[django.core.validators.RegexValidator(message='Text contains invalid character', regex='[a-zA-Z0-9 /{}\\$%_-~@#%\\^&\\(\\)!\\?\\\\]*')]),
        ),
        migrations.AlterField(
            model_name='chat',
            name='status',
            field=models.IntegerField(choices=[(1, 'NEW'), (2, 'SENT')], default=1),
        ),
        migrations.AlterField(
            model_name='conversation',
            name='status',
            field=models.IntegerField(choices=[(1, 'PENDING'), (2, 'RESOLVED')], default=1),
        ),
    ]