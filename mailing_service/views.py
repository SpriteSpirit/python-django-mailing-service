import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from mailing_service.forms import MailingForm, MessageForm, ClientForm
from mailing_service.models import Client, Message, Mailing, MailingLogs
from mailing_service.services import MailingService, send_mailing
from mailing_service.templatetags.custom_filters import translate_month_from_num
from django.contrib.auth.mixins import UserPassesTestMixin


# class ModeratorRequiredMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.groups.filter(name='Moderator').exists()


@login_required
def dashboard(request):
    user = request.user
    mailing_list = Mailing.objects.filter(user=user)

    today = timezone.now().date()
    now_month = timezone.now().month
    now_year = timezone.now().year

    month_mailing_count_list = [0] * 12
    last_week = [(today - timedelta(days=i - 1)).strftime('%d.%m') for i in range(7, 0, -1)]
    last_half_year = [translate_month_from_num((today - relativedelta(months=i - 1)).month) for i in range(6, 0, -1)]
    mailing_per_day = dict.fromkeys(last_week, 0)
    clients_added_half_year = dict.fromkeys(last_half_year, 0)

    for client in Client.objects.filter(user=user):
        month_client_added = translate_month_from_num(client.added_at.month)

        if client.added_at.year == now_year and month_client_added in last_half_year:
            clients_added_half_year[month_client_added] = clients_added_half_year.get(month_client_added, 0) + 1

    clients_added_half_year = list(clients_added_half_year.values())

    for mail in mailing_list:
        datetime_str = mail.first_send.strftime("%d/%m/%Y %H:%M:%S")
        date, time = datetime_str.split()
        month = int(date.split('/')[1][-1])
        mailing_year = int(date.split('/')[2])

        if mailing_year == now_year:
            for i in range(12):
                if i == month:
                    month_mailing_count_list[i - 1] += 1

        if mail.first_send.month == timezone.now().month:
            for i in range(7):
                day_ago = (today - timedelta(days=i)).strftime('%d.%m')

                if day_ago == mail.first_send.date().strftime('%d.%m'):
                    mailing_per_day[day_ago] = mailing_per_day.get(day_ago, 0) + 1

    mailing_per_day = list(mailing_per_day.values())
    now_month = translate_month_from_num(now_month)
    print(clients_added_half_year)
    context = {
        'active_page': 'dashboard',
        'mailing_list': mailing_list,
        'client_list': [mail.client.all().filter(user=user) for mail in mailing_list],
        'mailing_per_day': mailing_per_day,
        'last_week': json.dumps(last_week, ensure_ascii=False),
        'month_mailing_count_list': month_mailing_count_list,
        'year': now_year,
        'now_month': json.dumps(now_month, ensure_ascii=False),
        'last_half_year': json.dumps(last_half_year, ensure_ascii=False),
        'clients_added_half_year': clients_added_half_year,
    }

    return render(request, 'mailing_service/dashboard.html', context)


class ClientListView(LoginRequiredMixin, ListView):
    """ Просмотр списка клиентов """
    model = Client
    extra_context = {'title': 'КЛИЕНТЫ'}

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'client_list'

        return context

    def get_queryset(self):
        """ Просмотр только своих климентов """
        user = self.request.user

        if user.is_superuser or user.is_staff:
            queryset = Client.objects.all()
        else:
            queryset = Client.objects.filter(user=user)

        return queryset


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """ Валидация формы"""
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = Client.objects.get(id=self.kwargs['pk'])

        return context


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        """ Валидация формы"""
        client = form.save(commit=False)
        client.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:client_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.object

        return context


class MailingListView(LoginRequiredMixin, ListView):
    """ Просмотр списка клиентов """
    model = Mailing
    extra_context = {'title': 'РАССЫЛКИ'}

    def get_queryset(self):
        """ Просмотр рассылок только своих клиентов """
        user = self.request.user

        if user.is_superuser or user.is_staff:
            queryset = Mailing.objects.all()
        else:
            queryset = Mailing.objects.filter(user=user, is_published=True)

        return queryset

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'mailing_list'

        return context


class MailingCreateView(LoginRequiredMixin, CreateView):
    """ Создание новой рассылки """
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Создание рассылки'}
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['initial'] = {
            'first_send': datetime.now(),
            'finish_send': datetime.now() + timedelta(days=7),  # или любое другое значение по вашему выбору
        }

        return kwargs

    def form_valid(self, form):
        """ Валидация формы """
        mailing = form.save(commit=False)
        mailing.user = self.request.user

        if not mailing.first_send:
            mailing.first_send = timezone.now()
        mailing.status = 'created'
        mailing.save()

        """ Если форма валидна, то отправляется сообщение """
        message_service = MailingService(mailing)

        mailing.status = 'started'
        mailing.save()

        # Создание и запуск таска для отправки рассылки
        super().form_valid(form)
        send_mailing(mailing)
        message_service.create_task()

        return super(MailingCreateView, self).form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['mail'] = self.object
        context['clients'] = self.object.client.all()

        return context


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    """ Редактирование новой рассылки """
    model = Mailing
    form_class = MailingForm
    extra_context = {'title': 'Редактирование рассылки'}
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        """ Валидация формы"""
        mailing = form.save(commit=True)
        mailing.user = self.request.user
        mailing.status = Mailing.STATUS_CHOICES[0][1]
        mailing.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['mail'] = self.object

        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    """ Создание нового сообщения """
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Создание письма'}
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        """ Валидация формы"""
        message = form.save(commit=False)
        message.user = self.request.user
        message.save()

        """ Если форма валидна, то отправляется сообщение"""

        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    """ Просмотр списка писем """
    model = Message
    extra_context = {'title': 'ПИСЬМА'}

    def get_queryset(self):
        """ Просмотр только своих сообщений"""
        user = self.request.user

        if user.is_superuser or user.is_staff:
            queryset = Message.objects.all()
        else:
            queryset = Message.objects.filter(user=user)

        return queryset

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'message_list'

        return context


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    extra_context = {'title': 'Информация о сообщении'}

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)

        return context


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    extra_context = {'title': 'Редактирование письма'}
    success_url = reverse_lazy('mailing:message_list')

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)

        return context


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingLogListView(LoginRequiredMixin, ListView):
    """ Просмотр логов рассылки """
    model = MailingLogs
    extra_context = {'title': 'Состояние отправки'}

    def get_context_data(self, **kwargs):
        """ Дополнительная информация """
        context = super().get_context_data(**kwargs)
        context['active_page'] = 'log_list'
        info = []
        clients_per_mailing = {}

        logs = self.get_queryset()

        for log in logs:
            mailing_pk = log.mailing.pk
            if mailing_pk not in clients_per_mailing:
                clients_per_mailing[mailing_pk] = list(log.mailing.client.all())

        for log in logs:
            mailing = log.mailing

            client = clients_per_mailing[mailing.pk]  # Выделяем следующего клиента

            if client:
                client = clients_per_mailing[mailing.pk].pop(0)
            else:
                continue

            info.append(
                {
                    'log': log,
                    'mailing': mailing,
                    'client': client,
                }
            )

        context['info_client'] = info

        return context

    def get_queryset(self):
        """ Просмотр логов только своих рассылок """
        user = self.request.user
        mailing = Mailing.objects.filter(user=user)

        if user.is_superuser or user.is_staff:
            queryset = MailingLogs.objects.all().order_by('-date_time')
        else:
            queryset = MailingLogs.objects.filter(mailing__in=mailing)

        return queryset
