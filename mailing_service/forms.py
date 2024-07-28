from django import forms
from mailing_service.models import Mailing, Message, Client


class FormStyleMixin:
    """ Применение стилей к форме """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if (not isinstance(field.widget, forms.CheckboxInput) and
                    not isinstance(field.widget, forms.CheckboxSelectMultiple)):
                field.widget.attrs['class'] = 'form-control'


class MailingForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания и редактирования рассылки """

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('is_active', 'status', 'is_published', 'user')

        widgets = {
            'first_send': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'finish_send': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            # 'client': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['client'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)

        clients = Client.objects.filter(user=user)

        if clients.exists():
            self.fields['client'].widget = forms.CheckboxSelectMultiple()
            self.fields['client'].queryset = clients
        else:
            self.fields['client'].widget = forms.TextInput(attrs={'value': 'Нет клиентов', 'readonly': True,
                                                                  'style': 'border: none; '
                                                                           'background-color: transparent;', })


class MessageForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания и редактирования сообщения """

    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('user',)


class ClientForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания и редактирования сообщения """

    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('user',)
