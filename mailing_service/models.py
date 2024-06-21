from django.db import models


NULLABLE = {'null': True, 'blank': True}


# Create your models here.
class Client(models.Model):
    """
    Клиент
    """
    objects = models.Manager()

    name = models.CharField(max_length=150, verbose_name='Фамилия Имя Отчество')
    email = models.EmailField(unique=True, verbose_name='Email')
    comment = models.TextField(verbose_name='Комментарий', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Действующий')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} [{self.email}]'


class Message(models.Model):
    """ Сообщение для рассылки """
    objects = models.Manager()

    message_subject = models.CharField(max_length=150, verbose_name='Тема письма')
    message_body = models.TextField(verbose_name='Тело письма')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ('message_subject',)

    def __str__(self):
        return f'{self.message_subject}'


class Mailing(models.Model):
    """ Рассылка """

    PERIODICITY_CHOICES = (
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    )

    STATUS_CHOICES = (
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('completed', 'Завершена'),
    )

    objects = models.Manager()

    first_send = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    finish_send = models.DateTimeField(verbose_name='Дата и время завершения рассылки', default='2025-01-01 00:00:00')
    periodicity = models.CharField(max_length=20, choices=PERIODICITY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус рассылки')

    client = models.ManyToManyField(Client, related_name='mailings', verbose_name='Клиент')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    is_published = models.BooleanField(default=False, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ('-first_send',)

    def __str__(self):
        return f'Рассылка: {self.pk} [{self.status}] [{self.is_published}]'

    def deactivate_post(self):
        """ Деактивация пост рассылки """
        self.is_published = False
        self.status = 'completed'
        self.save()


class MailingLogs(models.Model):
    """ Логи рассылки """
    STATUS = [
        ('success', 'Успешно'),
        ('failed', 'Неудачно'),
    ]

    objects = models.Manager()

    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=100, choices=STATUS, verbose_name='Статус отправки')
    server_response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка', **NULLABLE)

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
        ordering = ('-date_time',)

    def __str__(self):
        return f'Лог рассылки: {self.pk} [{self.status}] [{self.mailing}][{self.server_response}]'
