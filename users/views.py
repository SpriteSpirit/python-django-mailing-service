from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserForm, UserRegisterForm, CustomAuthenticationForm
from users.models import User


class CreateUserView(CreateView):
    """
    Создание нового пользователя
    """
    model = User
    form_class = UserForm
    success_url = reverse_lazy('main:index')


def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('main:index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
