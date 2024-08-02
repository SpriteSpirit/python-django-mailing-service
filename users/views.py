import secrets
from random import randint

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from mailing_service.models import Client
from users.forms import UserForm, UserRegisterForm, CustomAuthenticationForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    """ Создание нового пользователя """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailing:dashboard')


def email_verification(token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    """ Редактирование информации пользователя """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        """ Валидация формы"""

        if form.is_valid:
            user = form.save(commit=True)
            user.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:profile', args=[self.kwargs.get('pk')])


class UserDetailView(DetailView):
    """ Просмотр профиля пользователя """
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.object
        context_data['clients'] = list(Client.objects.filter(user=user))
        print(list(context_data['clients'])[-1:-4:-1])

        return context_data


def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            # выполняем аутентификацию
            user = authenticate(email=email, password=password)
            login(request, user)

            return HttpResponseRedirect('users:profile')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('mailing:dashboard')


class CustomLogoutView(LogoutView):
    form_class = CustomAuthenticationForm
    template_name = 'users/logout.html'
    next_page = reverse_lazy('main:index')
    # success_url = reverse_lazy('main:index')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Просмотр списка пользователей """
    model = User
    extra_context = {'title': 'ПОЛЬЗОВАТЕЛИ'}
    permission_required = 'auth.can_view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all().order_by('last_name', 'first_name', 'id')
        context['active_page'] = 'user_list'

        return context

    def get_queryset(self):
        """ Просмотр только своих пользователей """
        print(self.request.user.get_user_permissions())
        print(self.request.user)

        return super().get_queryset()

    @staticmethod
    def post(request):
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)

        if user.is_staff and user.is_superuser:
            return render(request, 'users/block_page.html')

        user.is_blocked = not user.is_blocked
        user.save()

        return redirect(reverse('users:user_list') + f'?highlight_user={user_id}')


class UserCheckBlockView(PermissionRequiredMixin, View):
    """ Отображение страницы блокировки пользователя """
    permission_required = 'can_block_user'

    @staticmethod
    def get(request):
        return render(request, 'users/block_page.html')


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = None
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        new_password = generate_password()
        user.set_password(new_password)
        user.save()

        # Token generation for password reset
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Prepare email content
        subject = 'Восстановление и сброс пароля'
        reset_link = self.request.build_absolute_uri(reverse_lazy('users:password_reset_confirm', args=[uid, token]))

        html_message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'uid': uid,
            'token': token,
            'site_name': 'MAILING SERVICE',
            'password': new_password,
            'reset_link': reset_link,
        })

        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email=EMAIL_HOST_USER, recipient_list=[user.email],
                  html_message=html_message)

        return redirect(reverse('users:password_reset_done'))


def generate_password():
    password = ''
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    for i in range(randint(8, 12)):
        password += secrets.choice(chars)

    return password

# def toggle_activity(request, pk):
#     user_item = get_object_or_404(User, pk=pk)
#
#     if user_item.is_active:
#         user_item.is_active = False
#         send_deactivate_email(user_item) # Вызов сервисной функции
#     else:
#         user_item.is_active = True
#
#     user_item.save()
#
#     return redirect(reverse('users:profile', args=[user_item.pk]))
