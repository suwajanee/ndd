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


@csrf_exempt
def api_edit_expired_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            category = req['category']
            details = req['details']

            if category == 'truck':
                for detail in details:
                    truck = Truck.objects.get(pk=detail['id'])
                    truck.tax_expired_date = detail['tax_expired_date'] or None
                    truck.pat_pass_expired_date = detail['pat_pass_expired_date'] or None
                    truck.save()
                return JsonResponse('Success', safe=False)
            elif category == 'chassis':
                for detail in details:
                    chassis = Chassis.objects.get(pk=detail['id'])
                    chassis.tax_expired_date = detail['tax_expired_date'] or None
                    chassis.save()
                return JsonResponse('Success', safe=False)
    
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_truck(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            data = req['truck']

            truck = Truck.objects.get(pk=data['id'])
            truck.number = data['number']
            truck.license_plate = data['license_plate']
            truck.manufacturer = Manufacturer.objects.get(pk=data['manufacturer'])
            truck.tax_expired_date = data['tax_expired_date'] or None
            truck.pat_pass_expired_date = data['pat_pass_expired_date'] or None
            truck.status = data['status']
            truck.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_chassis(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            data = req['chassis']

            chassis = Chassis.objects.get(pk=data['id'])
            chassis.number = data['number']
            chassis.license_plate = data['license_plate']
            chassis.manufacturer = Manufacturer.objects.get(pk=data['manufacturer'])
            chassis.tax_expired_date = data['tax_expired_date'] or None
            chassis.status = data['status']
            chassis.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

            

                

