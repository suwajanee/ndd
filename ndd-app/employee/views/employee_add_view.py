# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Driver
from ..models import Employee
from ..models import Job
from ..models import Salary


@csrf_exempt
def api_add_employee(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            emp_data = req['emp_data']

            job_title = emp_data['job']
            job = Job.objects.get(job_title=job_title)
            
            data = {
                'first_name': emp_data['first_name'],
                'last_name': emp_data['last_name'],
                'birth_date': emp_data['birth_date'] or None,
                'detail': {
                    'tel': emp_data['tel'],
                    'account': emp_data['account']
                },
                'hire_date': emp_data['hire_date'] or None,
                'job': job,
                'status': 'active'
            }

            employee = Employee(**data)
            employee.save()

            add_employee_starting_salary(employee, emp_data['salary'])

            if job_title == 'driver':
                add_employee_driver(employee, emp_data)

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)


def add_employee_starting_salary(emp, salary):  
    data = {
        'employee': emp,
        'salary': float(salary) or 0,
        'from_date': emp.hire_date or datetime.now()
    }

    salary = Salary(**data)
    salary.save()

    return salary

def add_employee_driver(emp, emp_data):
    data = {
        'employee': emp,
        'license_type': emp_data['license_type'] or '3',
        'pat_pass_expired_date': emp_data['pat_pass_expired_date'] or None
    }

    driver = Driver(**data)
    driver.save()

    return driver