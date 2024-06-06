from django.shortcuts import render


def index(request):
    return render(request, 'main/index.html')


def clients(request):
    return render(request, 'main/clients.html')


def dashboard(request):
    return render(request, 'main/dashboard.html')


def about(request):
    return render(request, 'main/about.html')
