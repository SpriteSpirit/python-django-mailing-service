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


@register.filter
def translate_month(value):
    months = {"Январь": "January", "Февраль": "February", "Март": "March", "Апрель": "April",
              "Май": "May", "Июнь": "June", "Июль": "July", "Август": "August",
              "Сентябрь": "September", "Октябрь": "October", "Ноябрь": "November", "Декабрь": "December"}

    for m_ru, m_en in months.items():
        if m_en == value:
            return m_ru
    return value


@register.filter
def translate_month_from_num(value):
    months = {"Январь": 1, "Февраль": 2, "Март": 3, "Апрель": 4,
              "Май": 5, "Июнь": 6, "Июль": 7, "Август": 8,
              "Сентябрь": 9, "Октябрь": 10, "Ноябрь": 11, "Декабрь": 12}

    for m_ru, m_num in months.items():
        if m_num == value:
            return m_ru
    return value


@register.filter
def translate_activity(value):
    if value:
        return "Активный"
    return "Неактивный"


@register.filter
def translate_user_activity(value):
    if value:
        return "Заблокирован"
    return "Разблокирован"


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
