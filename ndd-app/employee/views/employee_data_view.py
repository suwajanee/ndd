# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Driver
from ..models import Employee
from ..models import Salary
from ..serializers import DriverSerializer
from ..serializers import EmployeeSerializer
from ..serializers import SalarySerializer


@csrf_exempt
def api_get_employee_count(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            
            officer = Employee.objects.filter(status='active', job__job_title='officer').count()
            driver = Employee.objects.filter(status='active', job__job_title='driver').count()
            mechanic = Employee.objects.filter(status='active', job__job_title='mechanic').count()

            not_active = Employee.objects.filter(status='terminated').count()

            data = {
                'emp': officer + driver + mechanic,
                'officer': officer,
                'driver': driver,
                'mechanic': mechanic,
                'not_active': not_active
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False) 

@csrf_exempt
def api_get_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            employee = Employee.objects.filter(status='active').order_by('job__number', 'hire_date', 'first_name', 'last_name')
            serializer = EmployeeSerializer(employee, many=True)
        
        elif request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            job = req['job']

            if job == 'driver':
                employee = Driver.objects.filter(employee__status='active').order_by('employee__hire_date', 'employee__first_name', 'employee__last_name')
                serializer = DriverSerializer(employee, many=True)
            else:
                employee = Employee.objects.filter(status='active', job__job_title=job).order_by('hire_date', 'first_name', 'last_name')
                serializer = EmployeeSerializer(employee, many=True)
        else:
            return JsonResponse('Error', safe=False)

        return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_not_active_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            employee = Employee.objects.filter(status='terminated').order_by('job__number', 'first_name', 'last_name')
            serializer = EmployeeSerializer(employee, many=True)
        
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_employee_salary(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            employee = Salary.objects.filter(employee__status='active').order_by('employee__job__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
            serializer = SalarySerializer(employee, many=True)
        
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)