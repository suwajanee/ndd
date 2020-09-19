# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Salary
from .employee_data_view import api_get_employee_salary


@csrf_exempt
def api_delete_latest_salary(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            latest_id = req['latest_id']
            old_id = req['old_id']

            Salary.objects.filter(pk=latest_id).delete()

            old_salary = Salary.objects.get(pk=old_id)
            old_salary.to_date = None
            old_salary.save()

            request.method = "GET"
            return api_get_employee_salary(request)
    return JsonResponse('Error', safe=False)

            