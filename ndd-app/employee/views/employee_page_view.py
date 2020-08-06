# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def employee_page(request):
    params = {
        'nbar': 'database-page',
        'title': 'Employee List',
    }
    return render(request, 'employee/employee_page.html', params)

@login_required(login_url=reverse_lazy('login'))
def employee_job_page(request, job):
    params = {
        'nbar': 'database-page',
        'title': job.title,
        'job': job,
    }
    return render(request, 'employee/employee_page.html', params)

@login_required(login_url=reverse_lazy('login'))
def former_employee_page(request):
    params = {
        'nbar': 'database-page',
        'page': 'former',
        'title': 'Former Employees'
    }
    return render(request, 'employee/employee_page.html', params)

@login_required(login_url=reverse_lazy('login'))
@permission_required('employee.change_salary', login_url=reverse_lazy('login'))
def employee_salary_page(request):
    params = {
        'nbar': 'database-page',
        'page': 'salary',
        'title': 'Salary'
    }
    return render(request, 'employee/employee_page.html', params)
 