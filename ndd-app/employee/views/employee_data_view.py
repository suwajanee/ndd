# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Driver
from ..models import Employee
from ..models import Job
from ..models import Salary
from ..serializers import DriverSerializer
from ..serializers import EmployeeSerializer
from ..serializers import JobSerializer
from ..serializers import SalarySerializer


@csrf_exempt
def api_get_job(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            job = Job.objects.all().order_by('number')
            serializer = JobSerializer(job, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False) 

@csrf_exempt
def api_get_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            data = get_employee_list('a')
            return JsonResponse(data, safe=False)
            
        elif request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            job = req['job']

            if job == 'driver':
                today = datetime.now()
                date_compare = today + timedelta(days=30)

                employee = Driver.objects.filter(employee__status='a').order_by('truck__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
                serializer = DriverSerializer(employee, many=True)
                data = {
                    'other': [],
                    'driver': serializer.data,
                    'date_compare': date_compare
                } 
            else:
                employee = Employee.objects.filter(status='a', job__job_title=job).order_by('hire_date', 'first_name', 'last_name')
                serializer = EmployeeSerializer(employee, many=True)
                data = {
                    'other': serializer.data,
                    'driver': [],
                }
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_former_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            data = get_employee_list('t')
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

# Salary
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
            req = json.loads(request.body.decode('utf-8'))
            emp_id = req['emp_id']

            salary = Salary.objects.filter(employee__pk=emp_id).order_by('-from_date', '-pk')
            serializer = SalarySerializer(salary, many=True)
        
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)


# Methods
def get_employee_list(status):
    employee = Employee.objects.filter(status=status)

    other = employee.filter(~Q(job__job_title='driver')).order_by('job__number', 'hire_date', 'first_name', 'last_name')
    other_serializer = EmployeeSerializer(other, many=True)

    driver = Driver.objects.filter(employee__in=employee).order_by('truck__number', 'employee__hire_date', 'employee__first_name', 'employee__last_name')
    driver_serializer = DriverSerializer(driver, many=True)

    data = {
        'other': other_serializer.data,
        'driver': driver_serializer.data
    }
    return data