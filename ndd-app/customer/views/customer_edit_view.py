# -*- coding: utf-8 -*-

import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import Principal, Shipper


class CustomerEditView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def edit_customer(request):
        if request.method == 'POST':
            pk = request.POST['pk']
            customer_name = request.POST['customer_edit']
            work_type = request.POST['work_type_edit']

            customer = Principal.objects.get(pk=pk)
            customer.name = re.sub(' +', ' ', customer_name.strip())
            customer.work_type = work_type
            customer.save()
            
            return redirect('customer-detail', pk=pk)
        else:
            return redirect('customer-list')

    @login_required(login_url=reverse_lazy('login'))
    def edit_shipper(request):
        if request.method == 'POST':
            customer_pk = request.POST['customer_pk']
            shipper_pk = request.POST['shipper_pk']
            shipper_name = request.POST['shipper_edit']
            address = request.POST['address_edit']

            shipper = Shipper.objects.get(pk=shipper_pk)
            shipper.name = re.sub(' +', ' ', shipper_name.strip())
            shipper.address = address
            shipper.save()
            
            return redirect('customer-detail', pk=customer_pk)
        else:
            return redirect('customer-list')

