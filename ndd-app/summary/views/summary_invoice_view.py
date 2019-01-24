# -*- coding: utf-8 -*-

import copy
import json
import re

from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from customer.models import Principal
from ..serializers import SummaryWeekSerializer, SummaryCustomerSerializer, InvoiceSerializer, CustomerCustomSerializer
from customer.serializers import PrincipalSerializer
from .summary_week_view import get_week_details
from .summary_customer_view import add_summary_customer


@csrf_exempt
def api_edit_invoice_remark(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            remarks = req['invoice_remark']

            for remark in remarks:

                invoice = Invoice.objects.get(pk=remark['id'])
                
                invoice.detail['remark'] = remark['detail']['remark']
                invoice.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_invoice_status(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['id']
            invoice_status = req['status']

            invoice = Invoice.objects.get(pk=invoice_id)

            invoice.status = invoice_status
            invoice.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

# Get invoice and summary_customer details
@csrf_exempt
def api_get_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = {}
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            week = req['week']
            customer = req['customer']
            if 'sub_customer' in req:
                sub_customer = req['sub_customer']

            if 'summary_customer' in req:
                summary_customer_pk = req['summary_customer']

            summary_customer = {}
            invoice = []

            week, data['week'] = get_week_details(week, year)
            if not week:
                return JsonResponse('Error', safe=False)

            try:
                summary_customer = SummaryCustomer.objects.get(pk=summary_customer_pk)
                invoice = Invoice.objects.filter(Q(customer_week=summary_customer)).order_by('invoice_no', 'pk')

                summary_customer_serializer = SummaryCustomerSerializer(summary_customer, many=False)
                data['summary_customer'] = summary_customer_serializer.data

                invoice_serializer = InvoiceSerializer(invoice, many=True)
                data['invoice'] = invoice_serializer.data
                    
            except:
                try:
                    customer_data = CustomerCustom.objects.get(Q(pk=sub_customer))
                    customer_custom_serializer = CustomerCustomSerializer(customer_data, many=False)
                    data['summary_customer'] = {'customer_custom': customer_custom_serializer.data} 
                except:
                    customer_data = Principal.objects.get(pk=customer)
                    customer_serializer = PrincipalSerializer(customer_data, many=False)
                    data['summary_customer'] = {'customer_main': customer_serializer.data}

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            summary_details = req['summary_details']
            # work_list = req['work_list']

            if 'summary_customer_id' in summary_details:
                print(summary_details)
                summary_customer = SummaryCustomer.objects.get(pk=summary_details['summary_customer_id'])
            else:
                summary_customer = add_summary_customer(summary_details)

            invoice_item = Invoice.objects.filter(customer_week=summary_customer).count()

            data = {
                'invoice_no': invoice_item + 1,
                'customer_week': summary_customer,
                'detail': {'remark': ''}
            }

            invoice = Invoice(**data)
            invoice.save()
            invoice_serializer = InvoiceSerializer(invoice, many=False)

            return JsonResponse(invoice_serializer.data, safe=False)
    return JsonResponse('Error', safe=False)