from django.template import Library
from datetime import datetime

register = Library()

@register.filter(name='parse_date')
def parse_date(value):
    return datetime.strptime(str(value), "%Y-%m-%d").strftime('%-d %b %y')