from django.shortcuts import render


def index(request):
    """ Главная страница сайта """
    return render(request, 'main/index.html')


def contacts(request):
    """ Страница контактов сайта """
    return render(request, 'main/contacts.html')


def noway_page(request):
    return render(request, 'main/noway_page.html')
