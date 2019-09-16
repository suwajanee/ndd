# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Driver
from ..models import Employee
from ..models import Job
from ..models import Salary
from truck.models import Truck


@csrf_exempt
def api_edit_employee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            emp_data = req['emp_data']

            status = emp_data['status']
            job_title = emp_data['job']

            emp = Employee.objects.get(id=emp_data['id'])
            emp.first_name = emp_data['first_name']
            emp.last_name = emp_data['last_name']
            emp.birth_date = emp_data['birth_date'] or None
            emp.detail = {
                'tel': emp_data['tel'],
                'account': emp_data['account']
            }
            emp.hire_date = emp_data['hire_date'] or None
            emp.status = status

            if status == 'a':
                emp.detail.pop("fire_date", None)
            else:
                emp.detail['fire_date'] = emp_data['fire_date'] or None

            emp.save()

            if job_title == 'driver':
                edit_employee_driver(emp_data)

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

def edit_employee_driver(emp_data):
    truck_id = emp_data['truck'] or None

    driver = Driver.objects.get(id=emp_data['driver_id'])
    driver.license_type = emp_data['license_type']
    driver.pat_pass_expired_date = emp_data['pat_pass_expired_date'] or None  
    driver.save()

    try:       
        old_truck = Truck.objects.get(pk=driver.truck.pk)
        old_truck.driver = None
        old_truck.save()
    except:
        pass

    if truck_id:
        truck = Truck.objects.get(pk=truck_id)
        truck.driver = driver
        truck.save()
    return driver

@csrf_exempt
def api_edit_pat_expired_driver(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            drivers = req['drivers']

            for driver in drivers:
                driver_data = Driver.objects.get(pk=driver['id'])
                driver_data.pat_pass_expired_date = driver['pat_pass_expired_date'] or None
                driver_data.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_employee_salary(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            salary_id = req['salary_id']
            emp_id = req['emp_id']
            new_salary = req['new_salary']

            today = datetime.now()

            old_salary = Salary.objects.get(pk=salary_id)
            old_salary.to_date = today
            old_salary.save()

            data = {
                'employee': Employee.objects.get(pk=emp_id),
                'salary': float(new_salary),
                'from_date': today
            }

            salary = Salary(**data)
            salary.save()


            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)