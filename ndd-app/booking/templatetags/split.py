from django.template import Library
from datetime import datetime

register = Library()

@register.filter(name='split')
def split(value, key):
    return value.split(key)

@register.filter(name='split_size')
def split_size(value, key):
    return value.split(key)[1]