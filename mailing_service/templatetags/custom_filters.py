from django import template
from mailing_service.models import Mailing

register = template.Library()


@register.filter
def translate_periodicity(value):
    for choice in Mailing.PERIODICITY_CHOICES:
        if choice[0] == value:
            return choice[1]
    return value


@register.filter
def translate_status(value):
    for choice in Mailing.STATUS_CHOICES:
        if choice[0] == value:
            return choice[1]
    return value
