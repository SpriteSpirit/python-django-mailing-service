from datetime import datetime

import pytz
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from config import settings
from mailing_service.models import MailingLogs


class MailingService:
    """ Сервис рассылки """

    def __init__(self, mailing):
        self.mailing = mailing

    def create_task(self):
        """ Создание задачи рассылки """
        crontab = self.crontab_create()
        PeriodicTask.objects.create(crontab=crontab, name=str(self.mailing), task='send_message',
                                    args=[self.mailing.pk])

    def crontab_create(self):
        """ Создание Crontab для выполнения периодических задач """
        print(type(self.mailing.first_send))

        if isinstance(self.mailing.first_send, str):
            datetime_obj = datetime.strptime(self.mailing.first_send, "%Y-%m-%d %H:%M:%S")
        else:
            datetime_obj = self.mailing.first_send

        date = datetime_obj.strftime("%Y-%m-%d")
        hour = datetime_obj.hour
        minute = datetime_obj.minute
        print(date, hour, minute)

        if self.mailing.PERIODICITY_CHOICES == 'daily':
            day_of_week = '*'
            day_of_month = '*'
        elif self.mailing.PERIODICITY_CHOICES == 'weekly':
            day_of_week = datetime_obj.weekday()
            day_of_month = '*'
        else:
            day_of_week = '*'
            day_of_month = datetime_obj.day if datetime_obj.day <= 28 else 28

        schedule, _ = CrontabSchedule.objects.get_or_create(minute=minute, hour=hour, day_of_week=day_of_week,
                                                            day_of_month=day_of_month, month_of_year='*')

        return schedule


def finish_task(mailing):
    """ Проверяет выполнена ли задача """
    end_time = mailing.first_send
    end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    current_time = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return current_time > str(end_time)


def delete_task(mailing):
    """ Удаление рассылки """
    task = PeriodicTask.objects.get(name=str(mailing))
    task.delete()
    mailing.status = 'completed'
    mailing.save()
    

def send_mailing(mailing):
    """ Отправка рассылки """
    message = mailing.message
    clients = mailing.client.all()

    for client in clients:
        try:
            print(f'Отправляем сообщение: {message.message_subject} ({message.message_body}) на email {client.email}')

            send_mail(
                subject=message.message_subject,
                message=message.message_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email],
                fail_silently=False
            )
            mailing_log = MailingLogs(
                date_time=datetime.now(),
                status='success',
                server_response='Сообщение отправлено!',
                mailing=mailing
            )
            print(mailing_log)
            mailing_log.save()

        except Exception as e:
            mailing_log = MailingLogs(
                date_time=datetime.now(),
                status='failed',
                server_response=f'Сообщение не было отправлено!\nОшибка: {e}',
                mailing=mailing
            )
            print(mailing_log)
            mailing_log.save()
