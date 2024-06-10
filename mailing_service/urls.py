from django.urls import path

from mailing_service.views import dashboard, ClientListView, MailingListView, MailingCreateView, MailingUpdateView, \
    MessageCreateView, MessageListView, ClientCreateView
from mailing_service.apps import MailingServiceConfig


app_name = MailingServiceConfig.name


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('create_mail/', MailingCreateView.as_view(), name='create_mail'),
    path('update_mail/<int:pk>/', MailingUpdateView.as_view(), name='update_mail'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
]
