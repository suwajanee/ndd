# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy


@login_required(login_url=reverse_lazy('login'))
def truck_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'truck', 'title': 'Truck', 'owner': 'ndd'})

@login_required(login_url=reverse_lazy('login'))
def sup_truck_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'truck', 'title': 'Truck', 'owner': 'vts'})


@login_required(login_url=reverse_lazy('login'))
def chassis_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'chassis', 'title': 'Chassis', 'owner': 'ndd'})

@login_required(login_url=reverse_lazy('login'))
def sup_chassis_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'chassis', 'title': 'Chassis', 'owner': 'vts'})


@login_required(login_url=reverse_lazy('login'))
def manufacturer_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'manufacturer', 'title': 'Manufacturer'})


@login_required(login_url=reverse_lazy('login'))
def sold_page(request):
    return render(request, 'truck/truck_page.html', {'nbar': 'database-page', 'page': 'sold', 'title': 'Sold', 'owner': 'ndd'})