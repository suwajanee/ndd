from django.template import Library
from datetime import datetime
import random


register = Library()

@register.filter(name='random_icon')
def random_icon(value):
    icon_list = ['cat', 'crow', 'dog', 'dove', 'dragon', 'fish', 'frog', 'hippo', 'horse', 'kiwi-bird', 'otter', 'spider']
    return random.choice(icon_list)