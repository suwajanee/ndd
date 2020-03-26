# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from employee.models import Employee
from summary.models import Year


@login_required(login_url=reverse_lazy('login'))
def daily_expense_page(request):
    date = datetime.now() - timedelta(days=1)
    if date.strftime('%w') == '0':
        date = date - timedelta(days=1)
    date = date.strftime('%Y-%m-%d/ndd')
    return HttpResponseRedirect('/report/daily-expense/' + date )

@login_required(login_url=reverse_lazy('login'))
def date_expense_page(request, date, co):
    if co != 'ndd' and co != 'vts':
        return HttpResponseRedirect('/dashboard')
    return render(request, 'transport_report/transport_report_daily_expense_page.html', {'nbar': 'report-page', 'title': 'Daily Expense', 'date': date, 'co': co})

@login_required(login_url=reverse_lazy('login'))
def driver_expense_page(request, date, driver):
    try:
        co = Employee.objects.get(pk=driver).co
    except:
        return HttpResponseRedirect('/dashboard')
    return render(request, 'transport_report/transport_report_daily_expense_page.html', {'nbar': 'report-page', 'title': 'Daily Expense', 'date': date, 'co': co, 'driver': driver})


@login_required(login_url=reverse_lazy('login'))
def expense_year_page(request, year):
    try:
        get_year = Year.objects.get(year_label=year)
    except:
        return HttpResponseRedirect('/dashboard')
    return render(request, 'transport_report/transport_report_expense_year_page.html', {'nbar': 'report-page', 'title': 'Expense', 'year': year})


@login_required(login_url=reverse_lazy('login'))
def monthly_expense_page(request):
    date = datetime.now().strftime('%Y/%m/ndd/')
    return HttpResponseRedirect('/report/expense/' + date)

@login_required(login_url=reverse_lazy('login'))
def expense_page(request, year, month, co):
    month = int(month)
    check_return = check_url_format(year, month, co)
    
    if check_return: 
        return render(request, 'transport_report/transport_report_expense_page.html', {'nbar': 'report-page', 'title': 'Expense', 'year': year, 'month': month, 'co': co, 'period': '0'})
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url=reverse_lazy('login'))
def period_expense_page(request, year, month, co, period):
    month = int(month)
    check_return = check_url_format(year, month, co)

    if check_return:
        return render(request, 'transport_report/transport_report_expense_page.html', {'nbar': 'report-page', 'title': 'Expense', 'year': year, 'month': month, 'co': co, 'period': period})
    else:
        return HttpResponseRedirect('/dashboard')


def check_url_format(year, month, co):
    try:
        get_year = Year.objects.get(year_label=year)
    except:
        return False

    if (month < 1 or month > 12) or (co != 'ndd' and co != 'vts'):
        return HttpResponseRedirect('/dashboard')
        return False
    return True