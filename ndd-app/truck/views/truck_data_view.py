# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
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
            available = Truck.objects.filter(status='available').count()
            maintanance = Truck.objects.filter(status='maintanance').count()

            data = {
                'available': available,
                'maintanance': maintanance,
                'total': available + maintanance
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
            data = {}
            truck = Truck.objects.filter(~Q(status='sold')).order_by('number')
            serializer = TruckSerializer(truck, many=True)

            data = {
                'truck': serializer.data,
                'date_compare': get_date_compare(7)
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_chassis(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            chassis = Chassis.objects.filter(~Q(status='sold')).order_by('number')
            serializer = ChassisSerializer(chassis, many=True)

            data = {
                'chassis': serializer.data,
                'date_compare': get_date_compare(7)
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_sold(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck = Truck.objects.filter(status='sold').order_by('number')
            chassis = Chassis.objects.filter(status='sold').order_by('number')

            truck_serializer = TruckSerializer(truck, many=True)
            chassis_serializer = ChassisSerializer(chassis, many=True)

            data = {
                'truck': truck_serializer.data,
                'chassis': chassis_serializer.data
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


def get_date_compare(date):
    today = datetime.now()
    date_compare = today + timedelta(days=date)
    return date_compare
