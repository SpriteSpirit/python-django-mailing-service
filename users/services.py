from django.core.mail import send_mail

from config import settings


def send_deactivate_email(user):
    send_mail(
        'Вас деактивировали',
        'Уважаемый пользователь, вас деактивировали. Обратитесь в поддержку',
        settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )


def is_moderator(user):
    return user.groups.filter(name='Moderator').exists()


def is_user(user):
    return not (user.is_superuser or user.is_staff)
