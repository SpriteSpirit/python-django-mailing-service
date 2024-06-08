from django.urls import path

from mailing_service.views import dashboard, ClientListView
from mailing_service.apps import MailingServiceConfig


app_name = MailingServiceConfig.name


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('clients/', ClientListView.as_view(), name='clients'),
]

