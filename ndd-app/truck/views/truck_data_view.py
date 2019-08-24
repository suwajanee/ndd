# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import TruckManufacturer
from ..models import Truck
from ..models import Chassis
from ..serializers import TruckSerializer
from ..serializers import ChassisSerializer


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

