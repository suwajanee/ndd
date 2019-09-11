# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
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
            officer = Employee.objects.filter(status='a', job__job_title='officer').count()
            driver = Employee.objects.filter(status='a', job__job_title='driver').count()
            mechanic = Employee.objects.filter(status='a', job__job_title='mechanic').count()

            terminated = Employee.objects.filter(status='t').count()
            terminated_driver = Driver.objects.filter(employee__status='t').count()

            data = {
                'emp': officer + driver + mechanic,
                'officer': officer,
                'driver': driver,
                'mechanic': mechanic,
                'active_except_driver': officer + mechanic,
                'terminated': terminated,
                'terminated_except_driver': terminated - terminated_driver
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False) 

@csrf_exempt
def api_get_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            employee = Employee.objects.filter(Q(status='a') & (Q(job__job_title='officer') | Q(job__job_title='mechanic'))).order_by('job__number', 'hire_date', 'first_name', 'last_name')
            emp_serializer = EmployeeSerializer(employee, many=True)

            driver = Driver.objects.filter(employee__status='a').order_by('employee__hire_date', 'employee__first_name', 'employee__last_name')
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
                today = datetime.now()
                date_compare = today + timedelta(days=7)

                employee = Driver.objects.filter(employee__status='a').order_by('truck__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
                serializer = DriverSerializer(employee, many=True)
                data = {
                    'emp': [],
                    'driver': serializer.data,
                    'date_compare': date_compare
                } 
            else:
                employee = Employee.objects.filter(status='a', job__job_title=job).order_by('hire_date', 'first_name', 'last_name')
                serializer = EmployeeSerializer(employee, many=True)
                data = {
                    'emp': serializer.data,
                    'driver': [],
                    'date_compare': ''
                }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_not_active_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":

            employee = Employee.objects.filter(Q(status='t') & (Q(job__job_title='officer') | Q(job__job_title='mechanic'))).order_by('job__number', 'first_name', 'last_name')
            emp_serializer = EmployeeSerializer(employee, many=True)

            driver = Driver.objects.filter(employee__status='t').order_by('employee__hire_date', 'employee__first_name', 'employee__last_name')
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

            employee = Salary.objects.filter(employee__status='a', to_date=None).order_by('employee__job__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
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
