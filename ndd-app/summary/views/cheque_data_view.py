# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import copy
import json

from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Invoice, SummaryCustomer, InvoiceDetail
from booking.views.utility.functions import set_if_not_none

@csrf_exempt
def api_get_cheque_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            month = req['month']
            date_from = req['date_from']
            date_to = req['date_to']
            mode = req['mode']

            today = datetime.now()
            filter_dict = {}
            if mode == 'due':
                set_if_not_none(filter_dict, 'date_due__year', year)
                set_if_not_none(filter_dict, 'date_due__month', month)
                set_if_not_none(filter_dict, 'date_due__gte', date_from)
                set_if_not_none(filter_dict, 'date_due__lte', date_to)
                summary_list = SummaryCustomer.objects.filter(**filter_dict).order_by('date_due', 'customer_main__name', 'customer_custom__sub_customer')
            elif mode == 'accept':
                set_if_not_none(filter_dict, 'date_accept__year', year)
                set_if_not_none(filter_dict, 'date_accept__month', month)
                set_if_not_none(filter_dict, 'date_accept__gte', date_from)
                set_if_not_none(filter_dict, 'date_accept__lte', date_to)
                summary_list = SummaryCustomer.objects.filter(**filter_dict).order_by('date_accept', 'customer_main__name', 'customer_custom__sub_customer')
            else:
                filter_dict = {
                    'date_due__lte': today,
                    'date_accept__isnull': True
                }  
                date_due = {
                    'date_due__month': month,
                    'date_due__year': year,
                }
                date_accept = {
                    'date_accept__month': month,
                    'date_accept__year': year
                }               
                summary_list = SummaryCustomer.objects.filter(Q(**filter_dict) | (~Q(**date_due) & Q(**date_accept))).order_by('date_due', 'customer_main__name', 'customer_custom__sub_customer')
                
            data_list = []
            for summary in summary_list:
                data = {}
                data = cheque_data_json(data, summary)
                data_list.append(data)

            due_total = cheque_month_total(year, month, 'date_due')
            accept_total = cheque_month_total(year, month, 'date_accept')

            response = {
                'detail': data_list,
                'today': today,
                'due_total': due_total,
                'accept_total': accept_total
            }
            return JsonResponse(response, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_cheque_accept_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            cheque_details = req['cheque_details']

            for detail in cheque_details:
                date_accept = detail['date_accept']

                summary_customer = SummaryCustomer.objects.get(pk=detail['id'])
                if not date_accept:
                    date_accept = None

                summary_customer.date_accept = date_accept
                summary_customer.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

# Method
def cheque_month_total(year, month, date):
    filter_dict = {
        date + '__year': year,
        date + '__month': month,
    }
    summary = SummaryCustomer.objects.filter(**filter_dict)
    invoice = Invoice.objects.filter(Q(customer_week__in=summary))

    drayage = invoice.aggregate(sum_drayage_total=Sum('drayage_total'))['sum_drayage_total']
    gate = invoice.aggregate(sum_gate_total=Sum('gate_total'))['sum_gate_total']
    if drayage or gate:
        drayage = float(drayage)
        gate = float(gate)
        total = (drayage + gate) - (drayage * (1/100))
    else:
        total = 0
    return total

def cheque_data_json(json, data):
    json['id'] = data.pk
    customer = data.customer_main

    json['customer'] = customer.name
    if data.customer_custom:
        if data.customer_custom.sub_customer:
            json['customer'] = data.customer_custom.sub_customer
    json['week'] = data.week.week
    json['date_billing'] = data.date_billing
    json['date_due'] = data.date_due
    json['due_month'] = data.date_due.month
    json['due_year'] = data.date_due.year
    json['date_accept'] = data.date_accept
    json['detail'] = data.detail
    json['status'] = data.status

    invoice = Invoice.objects.filter(Q(customer_week = data)).order_by('invoice_no')
    inv_list = []
    for inv in invoice:
        inv_list.append(inv.invoice_no)

    json['view_detail'] = False
    json['invoice'] = inv_list

    detail_list = InvoiceDetail.objects.filter(Q(invoice__customer_week=data))
    if customer.work_type == 'normal':
        container_1 = detail_list.filter(~Q(work_normal__size__contains='2X')).count()
        container_2 = detail_list.filter(Q(work_normal__size__contains='2X')).count()*2
        json['container'] = container_1 + container_2
    else:
        container_e_1 = detail_list.filter(Q(work_agent_transport__work_type='ep') & ~Q(work_agent_transport__size__contains='2X')).count()
        container_e_2 = detail_list.filter(Q(work_agent_transport__work_type='ep') & Q(work_agent_transport__size__contains='2X')).count()*2

        container_f_1 = detail_list.filter(Q(work_agent_transport__work_type='fc') & ~Q(work_agent_transport__size__contains='2X')).count()
        container_f_2 = detail_list.filter(Q(work_agent_transport__work_type='fc') & Q(work_agent_transport__size__contains='2X')).count()*2

        container_e = container_e_1 + container_e_2
        container_f = container_f_1 + container_f_2

        json['container'] = ''
        if container_e > 0:
            json['container'] += str(container_e) + 'E'
        if container_e > 0 and container_f > 0:
            json['container'] += '/'
        if container_f > 0:
            json['container'] += str(container_f) + 'F'          

    drayage_total = invoice.aggregate(sum_drayage_total=Sum('drayage_total'))['sum_drayage_total']
    gate_total = invoice.aggregate(sum_gate_total=Sum('gate_total'))['sum_gate_total']
    if drayage_total or gate_total:
        drayage_total = float(drayage_total)
        gate_total = float(gate_total)
        json['total'] = (drayage_total + gate_total) - (drayage_total * (1/100))
    else:
        json['total'] = 0

    return json