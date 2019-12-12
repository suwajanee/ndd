# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def daily_expense_page(request):
    return render(request, 'transport_report/daily_expense_page.html', {'nbar': 'transport-report-page', 'co': 'ndd'})

@login_required(login_url=reverse_lazy('login'))
def date_expense_page(request, date, co):
    return render(request, 'transport_report/daily_expense_page.html', {'nbar': 'transport-report-page', 'date': date, 'co': co})