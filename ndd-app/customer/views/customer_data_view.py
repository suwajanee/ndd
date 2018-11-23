# -*- coding: utf-8 -*-

from collections import OrderedDict
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Principal, Shipper, ShipperAddress
from ..serializers import PrincipalSerializer, ShipperSerializer, ShipperAddressSerializer


@csrf_exempt
def api_get_principals(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        work_type = req['work_type']
        
        principals = Principal.objects.filter(Q(work_type=work_type) & Q(cancel=0)).order_by('name')

    else:
        principals = Principal.objects.all().order_by('cancel', 'name')

    serializer = PrincipalSerializer(principals, many=True)

    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def api_get_shippers(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        principal_id = req['principal']

        shippers = Shipper.objects.filter(Q(principal=principal_id) & Q(cancel=0)).order_by('name')

    else:
        shippers = Shipper.objects.all().order_by('cancel', 'name')

    serializer = ShipperSerializer(shippers, many=True)

    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def api_get_shipper_address(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        shipper_id = req['shipper_id']
        
        shipper_address = ShipperAddress.objects.filter(shipper=shipper_id).order_by('address_type')
        serializer = ShipperAddressSerializer(shipper_address, many=True)

        return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_customer_details(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        principal_id = req['principal']

        shippers_pk = Shipper.objects.filter(principal=principal_id).values_list('pk')
        shipper = Shipper.objects.filter(pk__in=shippers_pk).order_by('name')
        shipper_serializer = ShipperSerializer(shipper, many=True)

        shipper_address = ShipperAddress.objects.filter(shipper__in=shippers_pk).order_by('shipper__cancel', 'shipper__name', 'address_type')
        shipper_address_serializer = ShipperAddressSerializer(shipper_address, many=True)
        shipper_address_data_list = shipper_address_serializer.data

        for shipper_data in shipper_serializer.data:
            address = any(shipper_address_data['shipper'] == shipper_data for shipper_address_data in shipper_address_serializer.data)
            if not address:      
                shipper_address_data_list.append(OrderedDict({'shipper': shipper_data}))

        return JsonResponse(shipper_address_data_list, safe=False)
    return JsonResponse('Error', safe=False)
