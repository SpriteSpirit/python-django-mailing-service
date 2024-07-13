from celery import shared_task
from mailing_service.models import Mailing
from mailing_service.services import finish_task, delete_task, send_mailing


@shared_task(name='send_message')
def send_message(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)
    clients = mailing.client.all()

    for client in clients:
        print(f'Отправка рассылки {mailing.message.message_subject} на email {client.email}')

    if finish_task(mailing):
        delete_task(mailing)
        return
    return send_mailing(mailing)

