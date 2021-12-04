# Generated by Django 3.2.9 on 2021-12-04 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0003_operator_operatorgroup'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_code', models.CharField(max_length=20)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversations.store')),
            ],
        ),
    ]