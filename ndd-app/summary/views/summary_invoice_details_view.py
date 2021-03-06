# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Invoice, InvoiceDetail
from ..serializers import InvoiceDetailSerializer
from booking.models import Booking
from booking.views.booking_data_view import booking_summary_status, booking_edit_summary
from booking.views.utility.functions import check_key_detail
from agent_transport.models import AgentTransport
from agent_transport.views.agent_transport_data_view import agent_transport_summary_status, agent_transport_edit_summary


@csrf_exempt
def api_get_invoice_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']

            invoice = Invoice.objects.get(pk=invoice_id)
            if 'order_by_remark' in invoice.detail:
                invoice_details = InvoiceDetail.objects.filter(invoice=invoice).order_by('work_normal__date', 'work_agent_transport__date', 'detail__remark', 'pk')
            else:
                invoice_details = InvoiceDetail.objects.filter(invoice=invoice).order_by('work_normal__date', 'work_agent_transport__date', 'pk')

            invoice_details_serializer = InvoiceDetailSerializer(invoice_details, many=True)

            return JsonResponse(invoice_details_serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

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
                for work_id in work_list:
                    work = Booking.objects.get(pk=work_id)
                    data = {
                        'invoice': invoice,
                        'work_normal': work,
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
                for work_id in work_list:
                    work = AgentTransport.objects.get(pk=work_id)
                    data = {
                        'invoice': invoice,
                        'work_agent_transport': work,
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

            invoice = save_invoice_total_charge(invoice, drayage_total, gate_total)

            invoice.detail = check_key_detail(invoice.detail, invoice_data, 'customer_name', True)
            invoice.detail = check_key_detail(invoice.detail, invoice_data, 'date_from', True)
            invoice.detail = check_key_detail(invoice.detail, invoice_data, 'other', True)
            invoice.detail = check_key_detail(invoice.detail, invoice_data, 'order_by_remark', True)

            invoice.save()

            for detail in invoice_detail_list:

                invoice_detail = InvoiceDetail.objects.get(pk=detail['id'])
                invoice_detail.drayage_charge['drayage'] = detail['drayage_charge']['drayage']

                if invoice_detail.gate_charge:
                    invoice_detail.gate_charge['gate'] = detail['gate_charge']['gate']
                    invoice_detail.gate_charge = check_key_detail(invoice_detail.gate_charge, detail['gate_charge'], 'vat', True)

                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'remark', False)
                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'remark_gate', True)
                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'note', True)

                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'routing', True)

                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'job_no', True)
                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'from', True)
                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'to', True)
                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'date', True)
                invoice_detail.detail = check_key_detail(invoice_detail.detail, detail['detail'], 'size', True)

                if 'other' in detail['drayage_charge']:
                    invoice_detail.drayage_charge = check_key_detail(invoice_detail.drayage_charge, detail['drayage_charge'], 'other', True)

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

@csrf_exempt
def api_delete_invoice_detail(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            invoice_id = req['invoice_id']
            invoice_detail_id = req['invoice_detail_id']
            customer_type = req['customer_type']

            invoice = Invoice.objects.get(pk=invoice_id)
            invoice = save_invoice_total_charge(invoice, req['drayage_total'], req['gate_total'])
            invoice.save()

            if 'work_id' in req:
                work_id = req['work_id']

                if 'copy' in invoice.detail:  
                    invoice_detail_id = InvoiceDetail.objects.filter(Q(work_agent_transport__pk=work_id) & Q(detail__has_key='copy'))
                else:
                    invoice_detail_id = InvoiceDetail.objects.filter(Q(work_agent_transport__pk=work_id) & ~Q(detail__has_key='copy'))

            status = delete_invoice_details(invoice_detail_id, customer_type)

            return api_get_invoice_details(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_check_container(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            
            invoice_detail_id = req['invoice_detail_id']
            index = str(req['index'])
            color = {'color'+index: req['color']}

            invoice_detail = InvoiceDetail.objects.get(pk=invoice_detail_id)
            invoice_detail.detail = check_key_detail(invoice_detail.detail, color, 'color'+index, True)
            invoice_detail.save()

            if 'color' + index in invoice_detail.detail:
                color_key = invoice_detail.detail['color'+index]
            else:
                color_key = 0

            return JsonResponse(color_key, safe=False)
    return JsonResponse('Error', safe=False)


# Method
def delete_invoice_details(invoice_detail, customer_type):
    if customer_type == 'normal':
        invoice_details = InvoiceDetail.objects.filter(pk__in=invoice_detail)
        work_list = invoice_details.values_list('work_normal', flat=True)
        
        if invoice_details and not 'copy' in invoice_details[0].detail:
            status = booking_summary_status(work_list, '0')
    
    elif customer_type == 'agent-transport':
        invoice_details = InvoiceDetail.objects.filter(pk__in=invoice_detail)
        work_list = invoice_details.values_list('work_agent_transport', flat=True)

        if invoice_details and not 'copy' in invoice_details[0].detail:
            status = agent_transport_summary_status(work_list, '0')

    invoice_details.delete()
    return True

def save_invoice_total_charge(invoice, drayage_total, gate_total):
    invoice.drayage_total = drayage_total
    if gate_total:
        invoice.gate_total = gate_total
    else:
        invoice.gate_total = 0
    return invoice
