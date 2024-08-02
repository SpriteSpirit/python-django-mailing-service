from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render

from config import settings


def index(request):
    """ Главная страница сайта """
    return render(request, 'main/index.html')


def contacts(request):
    """ Страница контактов сайта """
    if request.method == 'POST':
        # Получение данных из формы
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        message_content = request.POST.get('message', '')

        # Вывод значений в консоль для отладки
        # print("Name:", name)
        # print("Email:", email)
        # print("Phone:", phone)
        # print("Company:", company)
        # print("Message:", message_content)

        # Проверка, что поля не пустые
        if not name or not email or not message_content:
            return HttpResponse('Пожалуйста, заполните все обязательные поля.')

        # Формирование сообщения
        message = f"""
               Имя: {name}
               Email: {email}
               Телефон: {phone}
               Компания: {company}
               Сообщение: {message_content}
               """

        # Отправка письма
        send_mail(
            'Сообщение от пользователя с сайта Mailing Service',
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
        )
        return render(request, 'main/success_send_message.html')

    return render(request, 'main/contacts.html')


def noway_page(request):
    return render(request, 'main/noway_page.html')
