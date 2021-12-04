# Generated by Django 3.2.9 on 2021-12-04 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0006_auto_20211204_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sending_date', models.DateTimeField()),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversations.chat')),
            ],
        ),
    ]