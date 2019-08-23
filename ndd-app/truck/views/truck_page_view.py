# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def truck_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'title': 'Employee'})