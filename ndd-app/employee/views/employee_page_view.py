# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def employee_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page'})

@login_required(login_url=reverse_lazy('login'))
def employee_officer_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'job': 'officer'})

@login_required(login_url=reverse_lazy('login'))
def employee_driver_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'job': 'driver'})

@login_required(login_url=reverse_lazy('login'))
def employee_mechanic_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page', 'job': 'mechanic'})
