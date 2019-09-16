# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Manufacturer


@csrf_exempt
def api_delete_manufacturer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            manu_id = req['id']

            manufacturer = Manufacturer.objects.get(pk=manu_id)
            manufacturer.delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)