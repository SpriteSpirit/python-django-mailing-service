from django.contrib import admin
from mailing_service.models import Client, Message


# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'is_active']
    list_filter = ['name', 'is_active']
    search_fields = ['name', 'email', 'comment']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_subject', 'message_body', 'sent_at']
    list_filter = ['message_subject', 'sent_at']
    search_fields = ['message_subject', 'sent_at']
    date_hierarchy = 'sent_at'
    ordering = ('-sent_at',)