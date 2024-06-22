# Generated by Django 5.0.6 on 2024-06-22 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_service', '0021_alter_mailing_finish_send_alter_mailing_first_send'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='finish_send',
            field=models.DateTimeField(blank=True, verbose_name='Дата и время завершения рассылки'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='first_send',
            field=models.DateTimeField(blank=True, verbose_name='Дата и время отправки'),
        ),
    ]
