from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from mailing_service.forms import MailingForm, MessageForm, ClientForm
from mailing_service.models import Client, Message, Mailing


def dashboard(request):
    mailing = Mailing.objects.filter(status='created').first()
    context = {
        'active_page': 'dashboard',
    }
    if mailing:
        # Получение связанного сообщения письма
        message = mailing.message
        context = {
            'active_page': 'dashboard',
            'object_list': Client.objects.all(),
            'message_subject': message.message_subject,
            'message_body': message.message_body,
            'send_data': mailing.first_send,
            'status': mailing.status,
        }
        print(context)
    return render(request, 'mailing_service/dashboard.html', context)


class ClientListView(ListView):
    """ Просмотр списка клиентов """
    model = Client
    extra_context = {'title': 'КЛИЕНТЫ'}

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'client_list'
        context['object_list'] = Client.objects.all()
        mailing = Mailing.objects.filter(status='created').first()

        if mailing:
            # Получение связанного сообщения письма
            message = mailing.message
            context['message_subject'] = message.message_subject
            context['message_body'] = message.message_body
            context['send_data'] = mailing.first_send
            context['status'] = mailing.status
            print(context['message_subject'])
            print(context['message_body'])
            print(context['send_data'])
            print(context['status'])
        else:
            context['message_subject'] = ''
            context['message_body'] = ''
            context['send_data'] = ''
            context['status'] = ''

            print(context['message_subject'])
            print(context['message_body'])
        return context

    # def get_queryset(self):
    #     """ Просмотр только своих климентов """
    # pass


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """ Валидация формы"""
        client = form.save(commit=False)
        client.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class MailingListView(ListView):
    """ Просмотр списка клиентов """
    model = Mailing
    extra_context = {'title': 'РАССЫЛКИ'}

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'mailing_list'
        context['mailing_list'] = Mailing.objects.filter(status=Mailing.STATUS_CHOICES[0][1]).order_by('-id')

        return context

    # def get_queryset(self):
    #     """ Просмотр только своих климентов """
    # pass


class MailingCreateView(CreateView):
    """ Создание новой рассылки """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_queryset(self):
        """ Создание рассылки только для своих клиентов"""
        pass

    def form_valid(self, form):
        """ Валидация формы"""
        mailing = form.save(commit=False)
        mailing.status = Mailing.STATUS_CHOICES[0][1]
        print(mailing.status)
        mailing.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['mail'] = self.object

        return context


class MailingUpdateView(UpdateView):
    """ Редактирование новой рассылки """
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    # def get_queryset(self):
    #     """ Редактирование рассылки только для своих клиентов"""
    #     pass

    def form_valid(self, form):
        """ Валидация формы"""
        mailing = form.save(commit=True)
        mailing.status = Mailing.STATUS_CHOICES[0][1]
        mailing.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['mail'] = self.object

        return context


class MessageCreateView(CreateView):
    """ Создание нового сообщения """
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """ Валидация формы"""
        message = form.save(commit=False)
        message.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class MessageListView(ListView):
    """ Просмотр списка писем """
    model = Message
    extra_context = {'title': 'ПИСЬМА'}

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'message_list'
        context['message_list'] = Message.objects.all()

        return context


class MessageDetailView(DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)

        return context


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)

        return context


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')
