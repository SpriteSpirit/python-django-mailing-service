from django.contrib.auth.forms import UserChangeForm, UserCreationForm, SetPasswordForm, PasswordResetForm, \
    AuthenticationForm
from django import forms
# from django.utils.translation import gettext_lazy as _

from mailing_service.forms import FormStyleMixin
from users.models import User


class UserForm(FormStyleMixin, UserChangeForm):
    """Форма для профиля пользователя"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number', 'email', 'country', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    """Форма для регистрации пользователя"""

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


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
