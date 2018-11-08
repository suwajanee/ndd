import json

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
def api_cancel_customer(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        customer_id = req['customer_id']
        cancel_status = req['cancel_status']
        
        customer = Principal.objects.get(pk=customer_id)
        customer.cancel = cancel_status
        
        customer.save()

    return JsonResponse(customer.pk, safe=False)

@csrf_exempt
def api_cancel_shipper(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        shipper_id = req['shipper_id']
        cancel_status = req['cancel_status']
        
        shipper = Shipper.objects.get(pk=shipper_id)
        shipper.cancel = cancel_status
        
        shipper.save()

    return JsonResponse('Success', safe=False)


class CustomerCancelView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def cancel_customer(request):
        if request.method == 'POST':
            customer_pk = request.POST['customer_pk']

            customer = Principal.objects.get(pk=customer_pk)
            if customer.cancel == '0':
                customer.cancel = '1'
            else:
                customer.cancel = '0'
            customer.save()
            
            return redirect('customer-detail', pk=customer_pk)
        else:
            return redirect('customer-list')

    @login_required(login_url=reverse_lazy('login'))
    def cancel_shipper(request):
        if request.method == 'POST':
            customer_pk = request.POST['customer_pk']
            shipper_pk = request.POST['shipper_pk']
            
            shipper = Shipper.objects.get(pk=shipper_pk)
            if shipper.cancel == '0':
                shipper.cancel = '1'
            else:
                shipper.cancel = '0'
            shipper.save()
            
            return redirect('customer-detail', pk=customer_pk)
        else:
            return redirect('customer-list')

