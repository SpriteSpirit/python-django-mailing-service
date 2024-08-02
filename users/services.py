from django.core.mail import send_mail

from config import settings


def send_deactivate_email(user):
    send_mail(
        'Вас деактивировали',
        'Уважаемый студент, вас деактивировали. Обратитесь в поддержку',
        settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )