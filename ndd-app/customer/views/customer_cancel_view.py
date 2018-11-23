# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Principal, Shipper, ShipperAddress
from ..serializers import PrincipalSerializer, ShipperSerializer, ShipperAddressSerializer


@csrf_exempt
def api_cancel_customer(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        customer_id = req['customer_id']
        cancel_status = req['cancel_status']
        
        customer = Principal.objects.get(pk=customer_id)
        customer.cancel = cancel_status
        customer.save()

        return JsonResponse(customer.pk, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_cancel_shipper(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        shipper_id = req['shipper_id']
        cancel_status = req['cancel_status']
        
        shipper = Shipper.objects.get(pk=shipper_id)
        shipper.cancel = cancel_status
        shipper.save()

        return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)
