from django.template import Library

register = Library()

@register.filter(name='booking_field_text')
def booking_field_text(value):
    text = {
        '00': 'BOOKING',
        '01': 'B/L',
        '02': 'ROUTING',
    }
    return text[value]