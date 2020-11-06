# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from employee.models import Employee
from summary.models import Year


@login_required(login_url=reverse_lazy('login'))
def re_daily_report_page(request):
    date = datetime.now() - timedelta(days=1)
    if date.strftime('%w') == '0':
        date = date - timedelta(days=1)
    date = date.strftime('%Y-%m-%d')
    return HttpResponseRedirect('/report/daily-report/' + date )

@login_required(login_url=reverse_lazy('login'))
def daily_report_page(request, date):
    params = {
        'nbar': 'report-page',
        'title': 'Daily Report',
        'date': date
    }
    return render(request, 'transport_report/transport_report_daily_report_page.html', params)

@login_required(login_url=reverse_lazy('login'))
def driver_report_page(request, date, driver):
    params = {
        'nbar': 'report-page',
        'title': 'Daily Report',
        'date': date,
        'driver': driver
    }
    return render(request, 'transport_report/transport_report_daily_report_page.html', params)


@login_required(login_url=reverse_lazy('login'))
def yearly_expense_page(request, year):
    try:
        get_year = Year.objects.get(year_label=year)
    except:
        return HttpResponseRedirect('/dashboard')

    params = {
        'nbar': 'report-page',
        'title': 'Expense',
        'page': 'expense',
        'year': year
    }
    return render(request, 'transport_report/transport_report_yearly_report_page.html', params)

@login_required(login_url=reverse_lazy('login'))
def yearly_summary_page(request, year):
    try:
        get_year = Year.objects.get(year_label=year)
    except:
        return HttpResponseRedirect('/dashboard')
    
    params = {
        'nbar': 'report-page',
        'title': 'Summary',
        'page': 'summary',
        'year': year
    }
    return render(request, 'transport_report/transport_report_yearly_report_page.html', params)

@login_required(login_url=reverse_lazy('login'))
def yearly_total_expense_page(request, year):
    try:
        get_year = Year.objects.get(year_label=year)
    except:
        return HttpResponseRedirect('/dashboard')

    params = {
        'nbar': 'report-page',
        'title': 'Total Expense',
        'page': 'total-expense',
        'year': year
    }
    return render(request, 'transport_report/transport_report_yearly_report_page.html', params)


@login_required(login_url=reverse_lazy('login'))
def re_expense_page(request):
    date = datetime.now().strftime('%Y/%m')
    return HttpResponseRedirect('/report/expense/' + date)

@login_required(login_url=reverse_lazy('login'))
def expense_page(request, year, month):
    month = int(month)
    check_return = check_url_format(year, month)
    
    if check_return: 
        params = {
            'nbar': 'report-page',
            'title': 'Expense',
            'year': year,
            'month': month,
            'period': '0'
        }
        return render(request, 'transport_report/transport_report_expense_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url=reverse_lazy('login'))
def period_expense_page(request, year, month, period):
    month = int(month)
    check_return = check_url_format(year, month)

    if check_return:
        params = {
            'nbar': 'report-page',
            'title': 'Expense',
            'year': year,
            'month': month,
            'period': period
        }
        return render(request, 'transport_report/transport_report_expense_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')


@login_required(login_url=reverse_lazy('login'))
def re_summary_page(request):
    date = datetime.now().strftime('%Y/%m')
    return HttpResponseRedirect('/report/summary/' + date)

@login_required(login_url=reverse_lazy('login'))
def report_summary_page(request, year, month):
    month = int(month)
    check_return = check_url_format(year, month)

    if check_return:
        params = {
            'nbar': 'report-page',
            'title': 'Summary',
            'year': year,
            'month': month,
            'period': '0'
        }
        return render(request, 'transport_report/transport_report_summary_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url=reverse_lazy('login'))
def period_summary_page(request, year, month, period):
    month = int(month)
    check_return = check_url_format(year, month)

    if check_return:
        params = {
            'nbar': 'report-page',
            'title': 'Summary',
            'year': year,
            'month': month,
            'period': period
        }
        return render(request, 'transport_report/transport_report_summary_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')


@login_required(login_url=reverse_lazy('login'))
def re_total_expense_page(request):
    date = datetime.now().strftime('%Y/%m')
    return HttpResponseRedirect('/report/total-expense/' + date) 

@login_required(login_url=reverse_lazy('login'))
def total_expense_page(request, year, month):
    month = int(month)
    check_return = check_url_format(year, month)

    if check_return:
        params = {
            'nbar': 'report-page',
            'title': 'Total Expense',
            'year': year,
            'month': month,
            'period': '0'
        }
        return render(request, 'transport_report/transport_report_total_expense_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url=reverse_lazy('login'))
def period_total_expense_page(request, year, month, period):
    month = int(month)
    check_return = check_url_format(year, month)

    if check_return:
        params = {
            'nbar': 'report-page',
            'title': 'Total Expense',
            'year': year,
            'month': month,
            'period': period
        }
        return render(request, 'transport_report/transport_report_total_expense_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url=reverse_lazy('login'))
def re_total_truck_page(request):
    date = datetime.now().strftime('%Y/%m')
    return HttpResponseRedirect('/report/total-truck/' + date)

@login_required(login_url=reverse_lazy('login'))
def total_truck_page(request, year, month):
    month = int(month)
    check_return = check_url_format(year, month)

    if check_return:
        params = {
            'nbar': 'report-page',
            'title': 'Total Truck',
            'year': year,
            'month': month
        }
        return render(request, 'transport_report/transport_report_total_truck_page.html', params)
    else:
        return HttpResponseRedirect('/dashboard')
        

def check_url_format(year, month):
    try:
        get_year = Year.objects.get(year_label=year)
    except:
        return False

    if (month < 1 or month > 12):
        return False
    return True