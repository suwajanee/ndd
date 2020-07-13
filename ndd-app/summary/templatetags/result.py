from django.template import Library

register = Library()

@register.filter(name='result')
def result(value):
    if value:
        value = str(value)
        result = eval(value)

        result = "{:,.2f}".format(result)

        result = str(result)

        return result
    return '-'

@register.filter(name='add_float')
def add_float(num1, num2):
    return num1 + num2

@register.filter(name='minus')
def minus(num1, num2):
    return num1 - num2

@register.filter(name='mod')
def mod(num1, num2):
    return num1 % num2