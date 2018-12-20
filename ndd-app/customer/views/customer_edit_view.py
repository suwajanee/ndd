# -*- coding: utf-8 -*-

import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Principal, Shipper, ShipperAddress
from ..serializers import PrincipalSerializer, ShipperSerializer, ShipperAddressSerializer


@csrf_exempt
def api_save_edit_customer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            data = req['customer']

            customer = Principal.objects.get(pk=data['id'])
            customer.name = re.sub(' +', ' ', data['name'].strip())
            customer.work_type = data['work_type']
            customer.save()
            
        return JsonResponse(customer.pk, safe=False)
    return JsonResponse('Error', safe=False)            

@csrf_exempt
def api_save_edit_shipper(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            shipper_detail = req['shipper_detail']
            shipper_address_detail = req['shipper_address_detail']
            shipper_address_id = req['address_id']

            shipper = Shipper.objects.get(pk=shipper_detail['id'])
            shipper.name = re.sub(' +', ' ', shipper_detail['name'].strip())
            shipper.save()

            old_address_id = ShipperAddress.objects.filter(shipper=shipper_detail['id']).values_list('pk', flat=True)
            for address_id in old_address_id:
                if address_id not in shipper_address_id:
                    shipper_address = ShipperAddress.objects.get(pk=address_id).delete()
                
            for address in shipper_address_detail:
                if 'id' in address:
                    shipper_address = ShipperAddress.objects.get(pk=address['id'])
                    shipper_address.address_type = re.sub(' +', ' ', address['type'].strip())
                    shipper_address.address = address['address']
                    shipper_address.save()
                else:
                    if address['type'].strip() == '' and address['address'].strip() == '':
                        continue
                    data = {
                        'shipper': Shipper.objects.get(pk=shipper_detail['id']),
                        'address_type': re.sub(' +', ' ', address['type'].strip()),
                        'address': address['address']
                    }
                    shipper_address = ShipperAddress(**data)
                    shipper_address.save()

        return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)            
