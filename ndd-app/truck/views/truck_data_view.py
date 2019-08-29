# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Manufacturer
from ..models import Truck
from ..models import Chassis
from ..serializers import ChassisSerializer
from ..serializers import ManufacturerSerializer
from ..serializers import TruckSerializer


@csrf_exempt
def api_get_truck_choices(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(~Q(status='sold')).order_by('number')
            serializer = TruckSerializer(truck, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_daily_trucks(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            active = Truck.objects.filter(status='active').count()
            repair = Truck.objects.filter(status='repair').count()

            data = {
                'active': active,
                'repair': repair,
                'total': active + repair
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_truck_chassis_count(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(~Q(status='sold')).count()
            chassis = Chassis.objects.filter(~Q(status='sold')).count()

            data = {
                'truck': truck,
                'chassis': chassis
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_manufacturer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            category = req['category']

            manufacturer = Manufacturer.objects.filter(category=category)
            serializer = ManufacturerSerializer(manufacturer, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_truck(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(~Q(status='sold')).order_by('number')
            serializer = TruckSerializer(truck, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_chassis(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            chassis = Chassis.objects.filter(~Q(status='sold')).order_by('number')
            serializer = ChassisSerializer(chassis, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)
