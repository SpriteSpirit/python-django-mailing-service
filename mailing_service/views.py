from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import render
from django.views.generic import ListView

from mailing_service.models import Client, Message


def dashboard(request):
    client_data = Client.objects.annotate(date=TruncDay('sent_at')).values('date').annotate(
        count=Count('id')).order_by('date')
    message_data = Message.objects.annotate(date=TruncDay('sent_at')).values('date').annotate(
        count=Count('id')).order_by('date')

    context = {
        'active_page': 'dashboard',
        'client_data': list(client_data),
        'message_data': list(message_data),
    }
    return render(request, 'mailing_service/dashboard.html', context)


class ClientListView(ListView):
    """ Просмотр списка клиентов """
    model = Client
    extra_context = {'title': 'КЛИЕНТЫ'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'clients'
        context['object_list'] = Client.objects.all()
        return context

