from django.template import Library

register = Library()

@register.filter(name='time_color')
def time_color(value):
    try:
        time = value.split('.')
        if int(time[0])>0 and int(time[0])<11:
            return "bg-warning"
    except:
        pass
    return 