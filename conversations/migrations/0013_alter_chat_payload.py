# Generated by Django 3.2.9 on 2021-12-06 09:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0012_alter_chat_payload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='payload',
            field=models.CharField(max_length=300, validators=[django.core.validators.RegexValidator(message='Text contains invalid character', regex='^[a-zA-Z0-9 /{}\\$%_-~@#%\\^&\\(\\)!\\?\\\\\\.]*$')]),
        ),
    ]
