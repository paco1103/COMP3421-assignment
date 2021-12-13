from django import template
import datetime

register = template.Library()

@register.filter
def age_calculate(birth_date):
    today = datetime.datetime.now()
    born = birth_date
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    if age < 0:
        return 0
    return age

@register.filter
def date_format_convert(birth_date):
    date = ('0' + str(birth_date.day)) if birth_date.day < 10 else birth_date.day
    month = ('0' + str(birth_date.month)) if birth_date.month < 10 else birth_date.month
    return str(birth_date.year) + '-' + str(month) + '-' + str(date)