# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy

from ..models import CustomerCustom, SummaryCustomer
from customer.models import Principal


@login_required(login_url=reverse_lazy('login'))
def summary_page(request):
    return render(request, 'summary/summary_page.html', {'nbar': 'finance', 'title': 'Summary', 'title': 'Summary'})

@login_required(login_url=reverse_lazy('login'))
def cheque_page(request):
    return render(request, 'summary/cheque_page.html', {'nbar': 'finance', 'title': 'Cheque'})


@login_required(login_url=reverse_lazy('login'))
def summary_form_setting_page(request):
    return render(request, 'summary/summary_form_setting_page.html', {'nbar': 'finance', 'title': 'Summary'})

@login_required(login_url=reverse_lazy('login'))
def summary_customer_custom_page(request):
    return render(request, 'summary/summary_customer_custom_page.html', {'nbar': 'finance', 'title': 'Summary'})

@login_required(login_url=reverse_lazy('login'))
def summary_chart_page(request, year):
    return render(request, 'summary/summary_chart_page.html', {'nbar': 'finance', 'title': 'Summary', 'year': year})


@login_required(login_url=reverse_lazy('login'))
def summary_year_details_page(request, year):
    return render(request, 'summary/summary_year_details_page.html', {'nbar': 'finance', 'title': 'Summary', 'year': year})

@login_required(login_url=reverse_lazy('login'))
def summary_month_details_page(request, year, month):
    return render(request, 'summary/summary_month_details_page.html', {'nbar': 'finance', 'title': 'Summary', 'year': year, 'month': month})

@login_required(login_url=reverse_lazy('login'))
def summary_week_details_page(request, year, month, week):
    return render(request, 'summary/summary_week_details_page.html', {'nbar': 'finance', 'title': 'Summary', 'year': year, 'month': month, 'week': week})

@login_required(login_url=reverse_lazy('login'))
def summary_invoice_page(request, year, month, week, customer):
    customer_text = []
    customer = customer.split('__')
    customer_main_name = Principal.objects.get(pk=customer[0]).name
    customer_text.append(customer_main_name)

    if customer[1] != '':
        sub_customer_name = CustomerCustom.objects.get(pk=customer[1]).sub_customer
        customer_text.append(sub_customer_name)
        try:  
            summary_customer = SummaryCustomer.objects.get(Q(customer_custom__pk=customer[1]) & Q(week__week=week) & Q(week__year__year_label=year)).pk
            customer.append(summary_customer)
        except:
            pass
    else:
        try:
            summary_customer = SummaryCustomer.objects.get(Q(customer_main__pk=customer[0]) & Q(week__week=week) & Q(week__year__year_label=year)).pk
            customer.append(summary_customer)
        except:
            pass

    return render(request, 'summary/summary_invoice_page.html', {'nbar': 'finance', 'title': 'Summary', 'year': year, 'month': month, 'week': week, 'customer': customer, 'customer_text': customer_text})

@login_required(login_url=reverse_lazy('login'))
@permission_required('employee.change_salary', login_url=reverse_lazy('login'))
def commission_page(request):
    return render(request, 'summary/commission_page.html', {'nbar': 'finance', 'title': 'ค่าชอ.'})