# -*- coding: utf-8 -*-

import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser

from ..models import Principal, Shipper, ShipperAddress
from ..serializers import PrincipalSerializer, ShipperSerializer, ShipperAddressSerializer


@csrf_exempt
def api_get_shipper_address(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        shipper_id = req['shipper_id']
        
        shipper_address = ShipperAddress.objects.filter(shipper=shipper_id).order_by('address_type')

        serializer = ShipperAddressSerializer(shipper_address, many=True)

    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def api_get_principals(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        work_type = req['work_type']
        
        principals = Principal.objects.filter(Q(work_type=work_type) & Q(cancel=0)).order_by('name')

        serializer = PrincipalSerializer(principals, many=True)

    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def api_get_shippers(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        principal_id = req['principal']

        shippers = Shipper.objects.filter(Q(principal=principal_id) & Q(cancel=0)).order_by('name')

        serializer = ShipperSerializer(shippers, many=True)

    return JsonResponse(serializer.data, safe=False)