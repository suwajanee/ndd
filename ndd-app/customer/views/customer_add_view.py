# -*- coding: utf-8 -*-

import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Principal, Shipper, ShipperAddress
from ..serializers import PrincipalSerializer, ShipperSerializer, ShipperAddressSerializer


@csrf_exempt
def api_save_add_customer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            data = req['customer']

            data['name'] = re.sub(' +', ' ', data['name'].strip())

            customer = Principal(**data)
            customer.save()
            
        return JsonResponse(customer.pk, safe=False)
    return JsonResponse('Error', safe=False)        

@csrf_exempt
def api_save_add_shipper(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            customer_id = req['customer_id']
            shipper_name = req['shipper_name']
            address_detail = req['address']

            data = {
                'principal': Principal.objects.get(pk=customer_id),
                'name': re.sub(' +', ' ', shipper_name.strip()),
            }
            shipper = Shipper(**data)
            shipper.save()

            for address in address_detail:
                if address['type'].strip() == '' and address['address'].strip() == '':
                    continue
                data = {
                    'shipper': Shipper.objects.get(pk=shipper.pk),
                    'address_type': re.sub(' +', ' ', address['type'].strip()),
                    'address': address['address']
                }
                shipper_address = ShipperAddress(**data)
                shipper_address.save()
            
        return JsonResponse(customer_id, safe=False)
    return JsonResponse('Error', safe=False)        
