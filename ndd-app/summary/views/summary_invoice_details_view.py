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
from booking.models import Booking
from agent_transport.models import AgentTransport
from ..serializers import SummaryWeekSerializer, SummaryCustomerSerializer, InvoiceSerializer, CustomerCustomSerializer, InvoiceDetailSerializer
from customer.serializers import PrincipalSerializer
from .summary_week_view import get_week_details
from .summary_customer_view import add_summary_customer, delete_summary_customer
from booking.views.booking_data_view import booking_summary_status
from agent_transport.views.agent_transport_data_view import agent_transport_summary_status


@csrf_exempt
def api_add_invoice_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            work_list = req['work_list']
            customer_type = req['customer_type']

            invoice = Invoice.objects.get(pk=invoice_id)
            
            if customer_type == 'normal':
                bookings = Booking.objects.filter(pk__in=work_list)
                for booking in bookings:
                    data = {
                        'invoice': invoice,
                        'work_normal': booking,
                        'drayage_charge': {
                            'drayage': '',
                        },
                        'gate_charge': {
                            'gate': '',
                        },
                        'detail': {
                            'remark': '',
                        },
                    }
                    invoice_detail = InvoiceDetail(**data)
                    invoice_detail.save()
                status = booking_summary_status(work_list, '1')
            elif customer_type == 'agent-transport':
                agent_transports = AgentTransport.objects.filter(pk__in=work_list)
                for agent_transport in agent_transports:
                    data = {
                        'invoice': invoice,
                        'work_agent_transport': agent_transport,
                        'drayage_charge': {
                            'drayage': '',
                        },
                        'gate_charge': {
                            'gate': '',
                        },
                        'detail': {
                            'remark': '',
                        },
                    }
                    invoice_detail = InvoiceDetail(**data)
                    invoice_detail.save()
                status = agent_transport_summary_status(work_list, '1')               

            # for work in work_list:
            #     if customer_type == 'agent-transport':
            #         data['work_agent_transport'] = AgentTransport.objects.get(pk=work)
            #     elif customer_type == 'normal':
            #         data['work_normal'] = Booking.objects.get(pk=work)

            return api_get_invoice_details(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_invoice_details_evergreen(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            work_list = req['work_list']

            evergreen_work = []

            invoice = Invoice.objects.get(pk=invoice_id)

            for work in work_list:
                work_order = work.split('_')
                work_id = work_order[0]
                work_container = work_order[1]

                work_object = AgentTransport.objects.get(pk=work_id)

                evergreen_work.append(work_id)
                
                data = {
                    'invoice': invoice,
                    'work_agent_transport': work_object,
                    'drayage_charge': {
                        'drayage': '',
                    },
                    'detail': {
                        'job_no': '',
                        'from': '',
                        'to': '',
                        'date': '',
                        'size': '',
                        'truck': '',
                    },
                }
                
                if work_container == '1':
                    data['detail']['container'] = work_object.container_1

                elif work_container == '2':
                    data['detail']['container'] = work_object.container_2

                invoice_detail = InvoiceDetail(**data)
                invoice_detail.save()
            
            evergreen_work = set(evergreen_work)
                
            status = agent_transport_summary_status(evergreen_work, '1')               

            return api_get_invoice_details(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_invoice_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']

            invoice_details = InvoiceDetail.objects.filter(invoice__pk=invoice_id).order_by('work_normal__date', 'work_agent_transport__date')
            invoice_details_serializer = InvoiceDetailSerializer(invoice_details, many=True)

            return JsonResponse(invoice_details_serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_delete_invoice_detail(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_detail_id = req['invoice_detail_id']
            customer_type = req['customer_type']

            status = delete_invoice_details(invoice_detail_id, customer_type)

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

def delete_invoice_details(invoice_detail, customer_type):
    if customer_type == 'normal':
        invoice_details = InvoiceDetail.objects.filter(pk__in=invoice_detail)
        work_list = invoice_details.values_list('work_normal', flat=True)

        status = booking_summary_status(work_list, '0')
    
    elif customer_type == 'agent-transport':
        invoice_details = InvoiceDetail.objects.filter(pk__in=invoice_detail)
        work_list = invoice_details.values_list('work_agent_transport', flat=True)

        status = agent_transport_summary_status(work_list, '0')

    invoice_details.delete()
    return True

