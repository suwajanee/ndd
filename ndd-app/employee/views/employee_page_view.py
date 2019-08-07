# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def employee_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'title': 'Employee'})

@login_required(login_url=reverse_lazy('login'))
def employee_officer_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'job': 'officer', 'title': 'Officer'})

@login_required(login_url=reverse_lazy('login'))
def employee_driver_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'job': 'driver', 'title': 'Driver'})

@login_required(login_url=reverse_lazy('login'))
def employee_mechanic_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'job': 'mechanic', 'title': 'Mechanic'})

@login_required(login_url=reverse_lazy('login'))
def employee_not_active_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'page': 'not_active', 'title': 'Don\'t Active'})

@login_required(login_url=reverse_lazy('login'))
@permission_required('salary.can_change', login_url=reverse_lazy('login'))
def employee_salary_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'page': 'salary', 'title': 'Salary'})


 