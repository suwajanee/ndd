# -*- coding: utf-8 -*-

import json

from django.db.models import Q
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
            not_active_driver = Driver.objects.filter(employee__status='terminated').count()

            data = {
                'emp': officer + driver + mechanic,
                'officer': officer,
                'driver': driver,
                'mechanic': mechanic,
                'active_except_driver': officer + mechanic,
                'not_active': not_active,
                'not_active_except_driver': not_active - not_active_driver
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False) 

@csrf_exempt
def api_get_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            employee = Employee.objects.filter(Q(status='active') & (Q(job__job_title='officer') | Q(job__job_title='mechanic'))).order_by('job__number', 'hire_date', 'first_name', 'last_name')
            emp_serializer = EmployeeSerializer(employee, many=True)

            driver = Driver.objects.filter(employee__status='active').order_by('employee__hire_date', 'employee__first_name', 'employee__last_name')
            driver_serializer = DriverSerializer(driver, many=True)

            data = {
                'emp': emp_serializer.data,
                'driver': driver_serializer.data
            }
            return JsonResponse(data, safe=False)
            
        elif request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            job = req['job']

            if job == 'driver':
                employee = Driver.objects.filter(employee__status='active').order_by('truck__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
                serializer = DriverSerializer(employee, many=True)
                data = {
                    'emp': [],
                    'driver': serializer.data
                } 
            else:
                employee = Employee.objects.filter(status='active', job__job_title=job).order_by('hire_date', 'first_name', 'last_name')
                serializer = EmployeeSerializer(employee, many=True)
                data = {
                    'emp': serializer.data,
                    'driver': []
                }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_not_active_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            employee = Employee.objects.filter(Q(status='terminated') & (Q(job__job_title='officer') | Q(job__job_title='mechanic'))).order_by('job__number', 'first_name', 'last_name')
            emp_serializer = EmployeeSerializer(employee, many=True)

            driver = Driver.objects.filter(employee__status='terminated').order_by('employee__hire_date', 'employee__first_name', 'employee__last_name')
            driver_serializer = DriverSerializer(driver, many=True)

            data = {
                'emp': emp_serializer.data,
                'driver': driver_serializer.data
            }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_employee_salary(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            employee = Salary.objects.filter(employee__status='active', to_date=None).order_by('employee__job__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
            serializer = SalarySerializer(employee, many=True)
        
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_salary_history(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            emp_id = req['emp_id']

            salary = Salary.objects.filter(employee__pk=emp_id).order_by('-from_date', '-pk')
            serializer = SalarySerializer(salary, many=True)
        
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)
