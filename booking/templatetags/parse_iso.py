from django.template import Library
from datetime import datetime

register = Library()

@register.filter(expects_localtime=True)
def parse_iso(value):
    if value:
        return datetime.strptime(value, "%Y-%m-%d")
    else:
        return datetime.now()