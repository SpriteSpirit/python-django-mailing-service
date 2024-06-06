from django.urls import path

from main.apps import MainConfig
from main.views import index, clients, dashboard, about

app_name = MainConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('clients/', clients, name='clients'),
    path('dashboard/', dashboard, name='dashboard'),
    path('about/', about, name='about'),
]
