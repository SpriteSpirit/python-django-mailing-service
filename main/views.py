from django.core.mail import send_mail
from django.shortcuts import render, redirect

from config.settings import EMAIL_HOST_USER


def index(request):
    """ Главная страница сайта """
    return render(request, 'main/index.html')


def contacts(request):
    """ Страница контактов сайта """
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')

        send_mail(
            'Сообщение с сайта',
            message=message,
            recipient_list=[EMAIL_HOST_USER],
            from_email=EMAIL_HOST_USER,
        )
        return redirect('main:index')  # заменить на URL благодарности
    return render(request, 'main/contacts.html')


def noway_page(request):
    return render(request, 'main/noway_page.html')
