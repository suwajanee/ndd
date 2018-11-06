# -*- coding: utf-8 -*-

import json
import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import Principal, Shipper, ShipperAddress
from ..serializers import PrincipalSerializer, ShipperSerializer, ShipperAddressSerializer


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def api_save_add_customer(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        data = req['customer']

        data['name'] = re.sub(' +', ' ', data['name'].strip())

        customer = Principal(**data)
        customer.save()
        
    return JsonResponse(customer.pk, safe=False)





class CustomerAddView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def add_customer(request):
        if request.method == 'POST':
            customer_name = request.POST['customer_add']
            work_type = request.POST['work_type_add']

            data = {
                'name': re.sub(' +', ' ', customer_name.strip()),
                'work_type': work_type
            }

            customer = Principal(**data)
            customer.save()
            
            return redirect('customer-detail', pk=customer.pk)
        else:
            return redirect('customer-list')

    @login_required(login_url=reverse_lazy('login'))
    def add_shipper(request):
        if request.method == 'POST':
            customer_pk = request.POST['customer_pk']
            shipper_name = request.POST['shipper_add']

            address_type = request.POST.getlist('address_type_add')
            address = request.POST.getlist('address_add')

            data = {
                'principal': Principal.objects.get(pk=customer_pk),
                'name': re.sub(' +', ' ', shipper_name.strip()),
                # 'address': address
            }

            shipper = Shipper(**data)
            shipper.save()

            for i in range(len(address_type)):

                if address_type[i].strip() == '' and address[i].strip() == '':
                    continue
                data = {
                    'shipper': Shipper.objects.get(pk=shipper.pk),
                    'address_type': re.sub(' +', ' ', address_type[i].strip()),
                    'address': address[i]
                }
                shipper_address = ShipperAddress(**data)
                shipper_address.save()

            
            return redirect('customer-detail', pk=customer_pk)
        else:
            return redirect('customer-list')

