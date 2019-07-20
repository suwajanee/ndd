# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Employee
from ..serializers import EmployeeSerializer


@csrf_exempt
def api_get_employee_count(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            
            officer = Employee.objects.filter(status='active', job__job_title='officer').count()
            driver = Employee.objects.filter(status='active', job__job_title='driver').count()
            mechanic = Employee.objects.filter(status='active', job__job_title='mechanic').count()

            data = {
                'emp': officer + driver + mechanic,
                'officer': officer,
                'driver': driver,
                'mechanic': mechanic
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False) 

@csrf_exempt
def api_get_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            # req = json.loads( request.body.decode('utf-8') )

            employee = Employee.objects.filter(status='active').order_by('job__number', 'first_name', 'last_name')
        
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            job = req['job']

            employee = Employee.objects.filter(status='active', job__job_title=job).order_by('job__number', 'first_name', 'last_name')

        serializer = EmployeeSerializer(employee, many=True)

        return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False) 