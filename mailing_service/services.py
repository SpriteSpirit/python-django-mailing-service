from datetime import datetime

import pytz
from django.core.cache import cache
from django.core.mail import send_mail
from django_celery_beat.models import PeriodicTask, CrontabSchedule

from config import settings
from mailing_service.models import MailingLogs, Mailing, Message, Client


class MailingService:
    """ Сервис рассылки """

    def __init__(self, mailing):
        self.mailing = mailing

    def create_task(self):
        """Создание периодической задачи"""
        if self.mailing.is_published:
            crontab = self.crontab_create()
            PeriodicTask.objects.create(crontab=crontab, name=str(self.mailing), task='send_message',
                                        args=[self.mailing.pk])

    def crontab_create(self):
        """ Создание Crontab для выполнения периодических задач """

        if isinstance(self.mailing.first_send, str):
            datetime_obj = datetime.strptime(self.mailing.first_send, "%Y-%m-%d %H:%M:%S")
        else:
            datetime_obj = self.mailing.first_send

        hour = datetime_obj.hour
        minute = datetime_obj.minute

        if self.mailing.PERIODICITY_CHOICES == 'daily':
            day_of_week = '*'
            day_of_month = '*'
        elif self.mailing.PERIODICITY_CHOICES == 'weekly':
            day_of_week = datetime_obj.weekday()
            day_of_month = '*'
        else:
            day_of_week = '*'
            day_of_month = datetime_obj.day if datetime_obj.day <= 28 else 28

        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=minute,
            hour=hour,
            day_of_week=str(day_of_week),
            day_of_month=str(day_of_month),
            month_of_year='*'
        )

        return schedule


def finish_task(mailing):
    """ Проверяет выполнена ли задача """
    end_time = mailing.first_send

    if isinstance(end_time, str):
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

    current_time = datetime.now(pytz.timezone('Europe/Moscow'))
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

    return current_time > end_time.strftime("%Y-%m-%d %H:%M:%S")


def delete_task(mailing):
    """ Удаление рассылки """
    task = PeriodicTask.objects.get(name=str(mailing))
    print(task)
    if task:
        task.delete()

    mailing.status = 'completed'
    mailing.save()


def send_mailing(mailing):
    """Отправка рассылки и создание лога рассылки"""
    message = mailing.message
    clients = mailing.client.all()
    print('Send mailing func')

    for client in clients:
        try:
            print(f"Отправка на email {client.email}")  # Добавьте эту строку для отладки

            send_mail(
                subject=message.message_subject,
                message=message.message_body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email]
            )
            mailing_log = MailingLogs(
                date_time=datetime.now(),
                status='success',
                server_response='Сообщение успешно отправлено',
                mailing=mailing,
            )
            mailing_log.save()
        except Exception as e:
            print(f"Сообщение не отправлено {client.email}: {e}")  # Добавьте эту строку для отладки
            mailing_log = MailingLogs(
                date_time=datetime.now(),
                status='failed',
                server_response=f'Сообщение не отправлено!\nError: {e}',
                mailing=mailing,
            )
            mailing_log.save()


def get_cached_mailings():
    """
    Чтобы избежать избыточного запроса к базе данных, можно использовать метод get_or_set(),
    который получает значение из кэша и, если его нет, помещает значение в кэш.

    Чтобы избежать гонки при чтении/записи можно использовать метод add(),
    который помещает значение в кэш только в случае, если значение не существует
    """
    # кеширование на 15 минут
    cache_timeout = 60 * 15
    cache_key = 'mailings'

    if settings.CACHE_ENABLED:
        mailings = cache.get_or_set(cache_key, Mailing.objects.all, cache_timeout)

        if not mailings:
            mailings = Mailing.objects.all()
            cache.add(cache_key, mailings, cache_timeout)
    else:
        mailings = Mailing.objects.all()

    print(f'Кэширование продуктов {cache.get(cache_key)}')

    return mailings


def get_cached_messages():
    # кеширование на 10 минут
    cache_timeout = 10 * 60

    cache_key = 'messages'
    messages = cache.get(cache_key)

    if not messages:
        messages = Message.objects.all()
        cache.set(cache_key, messages, cache_timeout)
    else:
        messages = Message.objects.all()

    print(f'Кэширование категорий {cache.get(cache_key)}')

    return messages


def get_cached_clients():
    # кеширование на 10 минут
    cache_timeout = 10 * 60

    cache_key = 'messages'
    clients = cache.get(cache_key)

    if not clients:
        clients = Client.objects.all()
        cache.set(cache_key, clients, cache_timeout)
    else:
        clients = Message.objects.all()

    print(f'Кэширование категорий {cache.get(cache_key)}')

    return clients
