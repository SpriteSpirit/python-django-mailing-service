from django.contrib.auth.forms import UserChangeForm, UserCreationForm, SetPasswordForm, PasswordResetForm, \
    AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from django_countries import countries
from django_countries.widgets import CountrySelectWidget

# from django.utils.translation import gettext_lazy as _

from mailing_service.forms import FormStyleMixin
from users.models import User


class UserForm(FormStyleMixin, UserChangeForm):
    """Форма для профиля пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'email', 'country', 'avatar')
        widgets = {
            'password': forms.PasswordInput(),
        }

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        required=True
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput,
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = None

    def clean_password2(self):
        """Проверка совпадения паролей"""
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise ValidationError("Пароли не совпадают")

        return password2

    def save(self, commit=True):
        """Сохранение пользователя с зашифрованным паролем"""
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class UserProfileForm(FormStyleMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'country', 'avatar', 'about_message',
                  'website', 'github', 'telegram')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

# class CustomPasswordResetForm(FormStyleMixin, PasswordResetForm):
#     """Форма для сброса пароля"""
#     email = forms.EmailField(
#         label=_("Email"),
#         max_length=50,
#         widget=forms.EmailInput(attrs={"autocomplete": "email"}),
#     )
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     class Meta:
#         model = User
#
#
# class PasswordResetConfirmForm(FormStyleMixin, SetPasswordForm):
#     """Форма для обновления пароля"""
#
#     class Meta:
#         model = User


class CustomAuthenticationForm(AuthenticationForm):
    # Здесь вы можете добавить дополнительную логику или поля
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Например, изменить атрибуты поля
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
