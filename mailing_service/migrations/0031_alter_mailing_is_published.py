# Generated by Django 5.0.6 on 2024-07-28 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_service', '0030_message_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='Опубликован'),
        ),
    ]
