import json

from django.core.management import BaseCommand
from mailing_service.models import Mailing, Client, Message, MailingLogs
from users.models import User


class Command(BaseCommand):
    help = 'Заполнение базы данными из JSON-файлов'

    @staticmethod
    def json_read_mailings(json_file_name):
        mailings = []

        # Здесь мы получаем данные из фикстур с рассылками
        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "mailing_service.mailing":
                    print(item.get('model'))
                    mailings.append(item)

        return mailings

    @staticmethod
    def json_read_clients(json_file_name):
        clients = []

        # Здесь мы получаем данные из фикстур с клиентами
        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "mailing_service.client":
                    clients.append(item)

        return clients

    @staticmethod
    def json_read_messages(json_file_name):
        messages = []

        # Здесь мы получаем данные из фикстур с клиентами
        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "mailing_service.message":
                    messages.append(item)

        return messages

    @staticmethod
    def json_read_users(json_file_name):
        users = []

        # Здесь мы получаем данные из фикстур с пользователями
        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "users.user":
                    users.append(item)

        return users

    @staticmethod
    def json_read_mailing_logs(json_file_name):
        mailing_logs = []

        # Здесь мы получаем данные из фикстур с пользователями
        with open(json_file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "mailing_service.mailing_logs":
                    mailing_logs.append(item)

        return mailing_logs

    def handle(self, *args, **options):

        # Удаление всех рассылок
        Mailing.objects.all().delete()
        # Удаление всех клиентов
        Client.objects.all().delete()
        # Удаление всех сообщений
        Message.objects.all().delete()
        # Удаление всех логов рассылки
        MailingLogs.objects.all().delete()
        # Удаление всех пользователей
        User.objects.all().delete()

        # Списки для хранения объектов
        mailing_for_create = []
        client_for_create = []
        message_for_create = []
        mailing_logs_for_create = []
        user_for_create = []

        # Задаем имя файла JSON
        json_name = "data_base.json"

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for user in Command.json_read_users(json_name):
            print(f"Состав {user}")
            user_for_create.append(User(pk=user['pk'],
                                        email=user['fields']['email'],
                                        first_name=user['fields']['first_name'],
                                        last_name=user['fields']['last_name'],
                                        middle_name=user['fields']['middle_name'],
                                        phone_number=user['fields']['phone_number'],
                                        avatar=user['fields']['avatar'],
                                        country=user['fields']['country'],
                                        about_message=user['fields']['about_message'],
                                        is_blocked=user['fields']['is_blocked'],
                                        ))

        # Создаем объекты в базе с помощью метода bulk_create()
        User.objects.bulk_create(user_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for client in Command.json_read_clients(json_name):
            print(f"Состав {client}")
            client_for_create.append(Client(pk=client['pk'],
                                            name=client['fields']['name'],
                                            email=client['fields']['email'],
                                            comment=client['fields']['comment'],
                                            is_active=client['fields']['is_active'],
                                            user=User.objects.get(pk=client['fields']['user']),
                                            added_at=client['fields']['added_at']
                                            ))

        # Создаем объекты в базе с помощью метода bulk_create()
        Client.objects.bulk_create(client_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for message in Command.json_read_messages(json_name):
            message_for_create.append(Message(pk=message['pk'],
                                              message_subject=message['fields']['message_subject'],
                                              message_body=message['fields']['message_body'],
                                              user=User.objects.get(pk=message['fields']['user'])
                                              ))

        # Создаем объекты в базе с помощью метода bulk_create()
        Message.objects.bulk_create(message_for_create)

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for mailing in Command.json_read_mailings(json_name):
            print(f"Состав {mailing}")
            mailing_for_create.append(Mailing(pk=mailing['pk'],
                                              created_at=mailing['fields']['created_at'],
                                              first_send=mailing['fields']['first_send'],
                                              finish_send=mailing['fields']['finish_send'],
                                              periodicity=mailing['fields']['periodicity'],
                                              status=mailing['fields']['status'],
                                              message=Message.objects.get(pk=mailing['fields']['message']),
                                              is_published=mailing['fields']['is_published'],
                                              user=User.objects.get(pk=mailing['fields']['user']),
                                              ))

        # Создаем объекты в базе с помощью метода bulk_create()
        Mailing.objects.bulk_create(mailing_for_create)

        # Теперь добавляем клиентов к каждому Mailing
        for mailing_data, mailing_obj in zip(Command.json_read_mailings(json_name), Mailing.objects.all()):
            client_ids = mailing_data['fields']['client']
            clients = Client.objects.filter(pk__in=client_ids)
            mailing_obj.client.set(clients)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for mailing_log in Command.json_read_mailing_logs(json_name):
            print(f"Состав {mailing_log}")
            mailing_log.append(MailingLogs(pk=mailing_log['pk'],
                                           date_time=mailing_log['fields']['date_time'],
                                           status=mailing_log['fields']['status'],
                                           server_response=mailing_log['fields']['server_response'],
                                           mailing=mailing_log['fields']['mailing'],
                                           ))

        # Создаем объекты в базе с помощью метода bulk_create()
        MailingLogs.objects.bulk_create(mailing_logs_for_create)
