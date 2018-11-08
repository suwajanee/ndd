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
def api_save_edit_customer(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        data = req['customer']

        customer = Principal.objects.get(pk=data['id'])
        customer.name = re.sub(' +', ' ', data['name'].strip())
        customer.work_type = data['work_type']

        customer.save()
        
    return JsonResponse(customer.pk, safe=False)

@csrf_exempt
def api_save_edit_shipper(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        customer_id = req['customer_id']
        shipper_detail = req['shipper_detail']
        shipper_address_detail = req['shipper_address_detail']
        shipper_address_id = req['address_id']

        shipper = Shipper.objects.get(pk=shipper_detail['id'])
        shipper.name = re.sub(' +', ' ', shipper_detail['name'].strip())
        shipper.save()

        old_address_id = ShipperAddress.objects.filter(shipper=shipper_detail['id']).values_list('pk', flat=True)
        for address_id in old_address_id:
            if address_id not in shipper_address_id:
                shipper_address = ShipperAddress.objects.get(pk=address_id).delete()
            
        for address in shipper_address_detail:
            if 'id' in address:
                shipper_address = ShipperAddress.objects.get(pk=address['id'])
                shipper_address.address_type = re.sub(' +', ' ', address['type'].strip())
                shipper_address.address = address['address']
                shipper_address.save()
            else:
                if address['type'].strip() == '' and address['address'].strip() == '':
                    continue
                data = {
                    'shipper': Shipper.objects.get(pk=shipper_detail['id']),
                    'address_type': re.sub(' +', ' ', address['type'].strip()),
                    'address': address['address']
                }
                shipper_address = ShipperAddress(**data)
                shipper_address.save()

    return JsonResponse(customer_id, safe=False)



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

            shipper_address_pk = request.POST.getlist('shipper_address_pk')
            address_type = request.POST.getlist('address_type_edit')
            address = request.POST.getlist('address_edit')

            shipper = Shipper.objects.get(pk=shipper_pk)
            shipper.name = re.sub(' +', ' ', shipper_name.strip())
            shipper.save()

            shipper_address_pk_old = ShipperAddress.objects.filter(shipper=shipper_pk).values_list('pk', flat=True)
            for pk in shipper_address_pk_old:
                if str(pk) not in shipper_address_pk:
                    shipper_address = ShipperAddress.objects.get(pk=pk)
                    shipper_address.delete()

            for i in range(len(address_type)):
                if address_type[i].strip() == '' and address[i].strip() == '':
                    continue
                if i < len(shipper_address_pk):
                    shipper_address = ShipperAddress.objects.get(pk=int(shipper_address_pk[i]))
                    shipper_address.address_type = re.sub(' +', ' ', address_type[i].strip())
                    shipper_address.address = address[i]
                    shipper_address.save()
                else:
                    data = {
                        'shipper': Shipper.objects.get(pk=shipper_pk),
                        'address_type': re.sub(' +', ' ', address_type[i].strip()),
                        'address': address[i]
                    }
                    shipper_address = ShipperAddress(**data)
                    shipper_address.save()
            
            return redirect('customer-detail', pk=customer_pk)
        else:
            return redirect('customer-list')

