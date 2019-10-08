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
from employee.models import Driver


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
            truck = Truck.objects.filter(~Q(status='s') & Q(owner='ndd')).count()
            chassis = Chassis.objects.filter(~Q(status='s') & Q(owner='ndd')).count()

            sub_truck = Truck.objects.filter(~Q(status='s') & Q(owner='vts')).count()
            sub_chassis = Chassis.objects.filter(~Q(status='s') & Q(owner='vts')).count()

            data = {
                'truck': truck,
                'chassis': chassis,
                'sub_truck': sub_truck,
                'sub_chassis': sub_chassis,
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_manufacturer(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            truck_manu = Manufacturer.objects.filter(category='t').order_by('name')
            chassis_manu = Manufacturer.objects.filter(category='c').order_by('name')

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
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            owner = req['owner']

            data = {}
            truck = Truck.objects.filter(~Q(status='s') & Q(owner=owner)).order_by('number')
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
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            owner = req['owner']

            chassis = Chassis.objects.filter(~Q(status='s') & Q(owner=owner)).order_by('number')
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
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            owner = req['owner']
            
            truck = Truck.objects.filter(Q(status='s') & Q(owner=owner)).order_by('number')
            chassis = Chassis.objects.filter(Q(status='s') & Q(owner=owner)).order_by('number')

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
