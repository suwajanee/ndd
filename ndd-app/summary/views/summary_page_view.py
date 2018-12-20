# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login-page'))
def summary_page(request):
    return render(request, 'summary/summary_page.html', {'nbar': 'summary-page'})

@login_required(login_url=reverse_lazy('login-page'))
def summary_form_setting_page(request):
    return render(request, 'summary/summary_form_setting_page.html', {'nbar': 'summary-page'})

@login_required(login_url=reverse_lazy('login-page'))
def summary_year_details_page(request, year):
    return render(request, 'summary/summary_year_details_page.html', {'nbar': 'summary-page', 'year': year})