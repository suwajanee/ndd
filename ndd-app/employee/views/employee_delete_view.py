# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Driver
from ..models import Employee
from ..models import Salary


@csrf_exempt
def api_delete_employee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            emp_id = req['emp_id']

            employee = Employee.objects.get(pk=emp_id)

            driver = Driver.objects.filter(employee=employee)
            salary = Salary.objects.filter(employee=employee)

            driver.delete()
            salary.delete()
            employee.delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)