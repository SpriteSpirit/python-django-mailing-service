from django import forms
from mailing_service.models import Mailing, Message, Client


class FormStyleMixin:
    """ Применение стилей к форме """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'


class MailingForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания и редактирования рассылки """

    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ('is_active', 'status', )


class MessageForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания и редактирования сообщения """

    class Meta:
        model = Message
        fields = '__all__'


class ClientForm(FormStyleMixin, forms.ModelForm):
    """ Форма создания и редактирования сообщения """

    class Meta:
        model = Client
        fields = '__all__'
