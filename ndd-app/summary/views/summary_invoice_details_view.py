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
from booking.views.booking_data_view import booking_summary_status, booking_edit_summary
from agent_transport.views.agent_transport_data_view import agent_transport_summary_status, agent_transport_edit_summary


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
                            'note': ''
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
                            'note': ''
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
                        'remark': '',
                        'note': ''
                    },
                }
                
                if work_container == '1':
                    data['detail']['container'] = 1

                elif work_container == '2':
                    data['detail']['container'] = 2

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
            invoice_id = req['invoice_id']
            invoice_detail_id = req['invoice_detail_id']
            customer_type = req['customer_type']
            if 'work_id' in req:
                work_id = req['work_id']    
                invoice_detail_id = InvoiceDetail.objects.filter(work_agent_transport__pk=work_id)

            status = delete_invoice_details(invoice_detail_id, customer_type)

            return api_get_invoice_details(request)
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


@csrf_exempt
def api_edit_invoice_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            invoice_data = req['invoice_data']
            invoice_detail_list = req['invoice_detail_list']
            customer_type = req['customer_type']

            drayage_total = req['drayage_total']
            gate_total = req['gate_total']

            works = []

            invoice = Invoice.objects.get(pk=invoice_id)
            invoice.invoice_no = invoice_data['invoice_no']
            invoice.drayage_total = drayage_total
            if gate_total:
                invoice.gate_total = gate_total

            invoice = check_key_detail(invoice, invoice_data, 'customer_name', True)
            invoice = check_key_detail(invoice, invoice_data, 'date_from', True)
            invoice = check_key_detail(invoice, invoice_data, 'other', True)

            invoice.save()

            for detail in invoice_detail_list:

                invoice_detail = InvoiceDetail.objects.get(pk=detail['id'])
                invoice_detail.drayage_charge['drayage'] = detail['drayage_charge']['drayage']

                if invoice_detail.gate_charge:
                    invoice_detail.gate_charge['gate'] = detail['gate_charge']['gate']

                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'remark', False)
                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'note', False)

                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'job_no', False)
                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'from', False)
                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'to', False)
                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'date', False)
                invoice_detail = check_key_detail(invoice_detail, detail['detail'], 'size', False)

                invoice_detail.save()

                if 'container' in detail['detail']:
                    container = detail['detail']['container']
                    if container == 1:
                        detail['work'].pop('container_2')
                    else:
                        detail['work'].pop('container_1')
                
                works.append(detail['work'])
            
            if customer_type == 'normal':
                booking_edit_summary(works)
            else:
                agent_transport_edit_summary(works)

            return api_get_invoice_details(request)
    return JsonResponse('Error', safe=False)


def check_key_detail(invoice, data, key, pop):
    
    try:
        if data[key]:
            invoice.detail[key] = data[key]
        else: 
            try:
                if pop:
                    invoice.detail.pop(key)
                else:
                    invoice.detail[key] = ''
            except:
                pass
    except:
        pass
    return invoice


