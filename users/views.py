from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from mailing_service.models import Client
from users.forms import UserForm, UserRegisterForm, CustomAuthenticationForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    """ Создание нового пользователя """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailing:dashboard')


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
    permission_required = 'can_view_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_list'] = User.objects.all().order_by('last_name', 'first_name', 'id')
        context['active_page'] = 'user_list'

        return context

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
