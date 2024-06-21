from django.urls import path

from mailing_service.views import dashboard, ClientListView, MailingListView, MailingCreateView, MailingUpdateView, \
    MessageCreateView, MessageListView, ClientCreateView, MessageDetailView, MessageUpdateView, MessageDeleteView, \
    MailingDetailView, MailingDeleteView, ClientDetailView, ClientUpdateView, ClientDeleteView, MailingLogListView
from mailing_service.apps import MailingServiceConfig


app_name = MailingServiceConfig.name


urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),

    path('client_list/', ClientListView.as_view(), name='client_list'),
    path('create_client/', ClientCreateView.as_view(), name='create_client'),
    path('view_client/<int:pk>', ClientDetailView.as_view(), name='view_client'),
    path('update_client/<int:pk>', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>', ClientDeleteView.as_view(), name='delete_client'),

    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('create_mail/', MailingCreateView.as_view(), name='create_mail'),
    path('view_mail/<int:pk>', MailingDetailView.as_view(), name='view_mail'),
    path('update_mail/<int:pk>/', MailingUpdateView.as_view(), name='update_mail'),
    path('delete_mail/<int:pk>/', MailingDeleteView.as_view(), name='delete_mail'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('create_message/', MessageCreateView.as_view(), name='create_message'),
    path('view_message/<int:pk>/', MessageDetailView.as_view(), name='view_message'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),

    path('log_list/', MailingLogListView.as_view(), name='log_list'),

]
