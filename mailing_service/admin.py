from django.contrib import admin
from mailing_service.models import Client, Message, Mailing


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'is_active']
    list_filter = ['name', 'is_active']
    search_fields = ['name', 'email', 'comment']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_subject', 'message_body']
    list_filter = ['message_subject']
    search_fields = ['message_subject']
    # date_hierarchy = 'sent_at'
    # ordering = ('-sent_at',)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ['first_send', 'periodicity','status']
    list_filter = ['first_send', 'status']
    search_fields = ['status']
    date_hierarchy = 'first_send'
    ordering = ('-first_send',)