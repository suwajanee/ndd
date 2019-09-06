# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def truck_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'truck', 'title': 'Truck'})

@login_required(login_url=reverse_lazy('login'))
def chassis_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'chassis', 'title': 'Chassis'})

@login_required(login_url=reverse_lazy('login'))
def sold_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'sold', 'title': 'Sold'})