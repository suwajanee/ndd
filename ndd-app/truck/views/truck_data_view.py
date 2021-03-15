# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from django.db.models import Case, When
from django.db.models import FloatField
from django.db.models import Q
from django.db.models.functions import Cast
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Manufacturer
from ..models import Truck
from ..models import Chassis
from ..serializers import ChassisSerializer
from ..serializers import ManufacturerSerializer
from ..serializers import TruckSerializer


@csrf_exempt
def api_check_truck_driver(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            truck_id = req['truck_id']

            truck = Truck.objects.filter(pk=truck_id)
            serializer = TruckSerializer(truck[0], many=False)

            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_daily_trucks(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            active = Truck.objects.filter(status='a').count()
            maintanance = Truck.objects.filter(status='m').count()

            data = {
                'active': active,
                'maintanance': maintanance,
                'total': active + maintanance
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_truck_chassis_count(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(~Q(status='s')).count()
            chassis = Chassis.objects.filter(~Q(status='s')).count()

            data = {
                'truck': truck,
                'chassis': chassis,
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_manufacturer(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck_manu = Manufacturer.objects.filter(category='t').order_by('pk')
            chassis_manu = Manufacturer.objects.filter(category='c').order_by('pk')

            truck_serializer = ManufacturerSerializer(truck_manu, many=True)
            chassis_serializer = ManufacturerSerializer(chassis_manu, many=True)

            data = {
                'truck_manu': truck_serializer.data,
                'chassis_manu': chassis_serializer.data
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_truck(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(~Q(status='s')).order_by('number')
            serializer = TruckSerializer(truck, many=True)

            data = {
                'truck': serializer.data,
                'date_compare': get_date_compare(30)
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_chassis(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            chassis = Chassis.objects.filter(~Q(status='s'))
            chassis = order_by_number_value(chassis, 'number')
            serializer = ChassisSerializer(chassis, many=True)

            data = {
                'chassis': serializer.data,
                'date_compare': get_date_compare(30)
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_sold(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(status='s').order_by('number')
            chassis = Chassis.objects.filter(status='s')
            chassis = order_by_number_value(chassis, 'number')

            truck_serializer = TruckSerializer(truck, many=True)
            chassis_serializer = ChassisSerializer(chassis, many=True)

            data = {
                'truck': truck_serializer.data,
                'chassis': chassis_serializer.data
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_active_truck(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(~Q(status='s')).order_by('number')
            serializer = TruckSerializer(truck, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)


# Methods
def get_date_compare(date):
    today = datetime.now()
    date_compare = today + timedelta(days=date)
    return date_compare

def order_by_number_value(data, key):
    data = data.annotate(number_float=Case(
        When(**{key + '__regex': r'^([\d]+)$'}, then=Cast(key, FloatField()))
    ))
    data = data.order_by('number_float', key)
    return data
