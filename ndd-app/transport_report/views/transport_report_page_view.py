# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from employee.models import Employee


@login_required(login_url=reverse_lazy('login'))
def expense_page(request):
    return render(request, 'transport_report/transport_report_daily_expense_page.html', {'nbar': 'transport-report-page', 'co': 'ndd'})

@login_required(login_url=reverse_lazy('login'))
def date_expense_page(request, date, co):
    return render(request, 'transport_report/transport_report_daily_expense_page.html', {'nbar': 'transport-report-page', 'date': date, 'co': co})

@login_required(login_url=reverse_lazy('login'))
def driver_expense_page(request, date, driver):
    try:
        co = Employee.objects.get(pk=driver).co
    except:
        return HttpResponseRedirect('/dashboard')
    return render(request, 'transport_report/transport_report_daily_expense_page.html', {'nbar': 'transport-report-page', 'date': date, 'co': co, 'driver': driver})