# Generated by Django 3.2.9 on 2021-12-05 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0009_auto_20211205_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chats', to='conversations.conversation'),
        ),
    ]