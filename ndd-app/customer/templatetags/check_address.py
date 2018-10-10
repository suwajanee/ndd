from django.template import Library
from ..models import Shipper, ShipperAddress

register = Library()

@register.filter(name='check_address')
def check_address(value):
    return ShipperAddress.objects.filter(shipper=value).order_by('address_type')