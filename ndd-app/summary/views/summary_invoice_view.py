# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import CustomerCustom, Invoice, InvoiceDetail, SummaryCustomer
from ..serializers import CustomerCustomSerializer, InvoiceSerializer, SummaryCustomerSerializer
from .summary_customer_view import add_summary_customer, delete_summary_customer
from .summary_invoice_details_view import delete_invoice_details
from .summary_week_view import get_week_details
from booking.views.utility.functions import check_key_detail
from customer.models import Principal
from customer.serializers import PrincipalSerializer


@csrf_exempt
def api_edit_invoice_remark(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            remarks = req['invoice_remark']

            for remark in remarks:
                invoice = Invoice.objects.get(pk=remark['id'])

                invoice.detail = check_key_detail(invoice.detail, remark['detail'], 'remark', True)
                
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
                customer_data = Principal.objects.get(pk=customer)
                customer_serializer = PrincipalSerializer(customer_data, many=False)
                data['summary_customer'] = {'customer_main': customer_serializer.data}
                try:
                    customer_data = CustomerCustom.objects.get(Q(pk=sub_customer))
                    customer_custom_serializer = CustomerCustomSerializer(customer_data, many=False)
                    data['summary_customer']['customer_custom'] = customer_custom_serializer.data
                except:
                    pass

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            summary_details = req['summary_details']

            if 'summary_customer_id' in summary_details:
                summary_customer = SummaryCustomer.objects.get(pk=summary_details['summary_customer_id'])
            else:
                summary_customer = add_summary_customer(summary_details)

            invoice_count = Invoice.objects.filter(customer_week=summary_customer).count()

            data = {
                'invoice_no': invoice_count + 1,
                'customer_week': summary_customer,
                'detail': {}
            }

            invoice = Invoice(**data)
            invoice.save()
            invoice_serializer = InvoiceSerializer(invoice, many=False)

            return JsonResponse(invoice_serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_invoice_week(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            summary_details = req['summary_details']

            data_summary_customer = {
                'week__pk': summary_details['week'],
                'customer_main__pk': summary_details['customer_main']
            }
            if 'customer_custom' in summary_details:
                data_summary_customer['customer_custom__pk'] = summary_details['customer_custom']

            summary_customer = SummaryCustomer.objects.filter(**data_summary_customer)

            if summary_customer:
                id_summary_customer = summary_customer[0].pk
            else:
                new_summary_customer = add_summary_customer(summary_details)
                id_summary_customer = new_summary_customer.pk

            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.customer_week = SummaryCustomer.objects.get(pk=id_summary_customer)
            invoice.save()

            check_summary_customer = delete_summary_customer(summary_details['summary_customer_id'])

            return JsonResponse(check_summary_customer, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_delete_invoice_week(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            summary_customer_id = req['summary_customer_id']
            customer_type = req['customer_type']

            invoice_details = InvoiceDetail.objects.filter(invoice__pk=invoice_id).values_list('pk', flat=True)
            delete_status = delete_invoice_details(invoice_details, customer_type)

            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.delete()

            check_summary_customer = delete_summary_customer(summary_customer_id)

            return JsonResponse(check_summary_customer, safe=False)
    return JsonResponse('Error', safe=False)


@csrf_exempt
def api_copy_invoice(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            invoice_detail_list = req['invoice_detail']

            invoice = Invoice.objects.get(pk=invoice_id)
            invoice_count = Invoice.objects.filter(customer_week=invoice.customer_week).count()
            invoice.pk = None
            invoice.invoice_no = invoice_count + 1
            invoice.status = 0
            invoice.detail['copy'] = True
            invoice.save()
            
            invoice_serializer = InvoiceSerializer(invoice, many=False)

            for detail in invoice_detail_list:
                invoice_detail = InvoiceDetail.objects.get(pk=detail['id'])
                invoice_detail.pk = None
                invoice_detail.invoice = invoice
                invoice_detail.detail['copy'] = True
                invoice_detail.save()

            return JsonResponse(invoice_serializer.data, safe=False)
    return JsonResponse('Error', safe=False)
