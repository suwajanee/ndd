from django.template import Library

register = Library()

@register.filter(name='result')
def result(value):
    if value:
        value = str(value)
        result = eval(value)

        result = "{:,}".format(result)

        result = str(result)
        x = result.split('.')

        if len(x) == 1:
            x.append('00')
        elif len(x[1]) == 1:
            x[1] = x[1] + '0'

        return x[0] + '.' + x[1]
    return '-'

@register.filter(name='minus')
def minus(num1, num2):
    return num1 - num2

@register.filter(name='mod')
def mod(num1, num2):
    return num1 % num2