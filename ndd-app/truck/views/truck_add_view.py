# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Chassis
from ..models import Manufacturer
from ..models import Truck
from ..serializers import ChassisSerializer
from ..serializers import ManufacturerSerializer
from ..serializers import TruckSerializer
from .truck_data_view import api_get_chassis, api_get_truck


@csrf_exempt
def api_add_truck(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            data = req['data']

            manufacturer = None
            if data['manufacturer']:
                manufacturer = Manufacturer.objects.get(pk=data['manufacturer'])

            truck_data = {
                'number': data['number'],
                'license_plate': data['license_plate'],
                'manufacturer': manufacturer,
                'tax_expired_date': data['tax_expired_date'] or None,
                'pat_pass_expired_date': data['pat_pass_expired_date'] or None,
                'status': 'a'
            }

            truck = Truck(**truck_data)
            truck.save()

            request.method = "GET"
            return api_get_truck(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_chassis(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            data = req['data']

            manufacturer = None
            if data['manufacturer']:
                manufacturer = Manufacturer.objects.get(pk=data['manufacturer'])

            chassis_data = {
                'number': data['number'],
                'license_plate': data['license_plate'],
                'manufacturer': manufacturer,
                'tax_expired_date': data['tax_expired_date'] or None,
                'status': 'a'
            }

            chassis = Chassis(**chassis_data)
            chassis.save()

            request.method = "GET"
            return api_get_chassis(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_manufacturer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = json.loads(request.body.decode('utf-8'))

            data['name'] = data['name'].title().strip()

            manufacturer = Manufacturer(**data)
            manufacturer.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)