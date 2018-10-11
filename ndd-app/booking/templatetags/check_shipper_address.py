from django.db.models import Q
from django.template import Library

from customer.models import Shipper, ShipperAddress


register = Library()

@register.filter(name='check_shipper_address')
def check_shipper_address(shipper, principal):
    try:
        shipper_pk = Shipper.objects.get(Q(principal__name=principal) & Q(name=shipper))
        return ShipperAddress.objects.filter(shipper=shipper_pk).order_by('address_type')

    except Shipper.DoesNotExist:
        return False