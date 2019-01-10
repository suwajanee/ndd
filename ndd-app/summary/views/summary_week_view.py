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
from ..serializers import SummaryWeekSerializer


@csrf_exempt
def api_check_week_exist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            week = req['week']

            week_existing = SummaryWeek.objects.filter(year__year_label=year, week=week)
            if week_existing:
                return JsonResponse(True, safe=False)
            return JsonResponse(False, safe=False)
            
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_summary_week(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            data = req['summary_week']

            data['year'] = Year.objects.get(year_label=data['year'])

            summary_week = SummaryWeek(**data)
            summary_week.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_summary_week(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            data = req['summary_week']

            data['year'] = Year.objects.get(year_label=data['year'])

            summary_week = SummaryWeek(**data)

            summary_week.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_summary_week_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            month = req['month']
            week = req['week']

            details = {}
            weeks = []

            week_existing = SummaryWeek.objects.filter(Q(year__year_label=year) & Q(week=week))
            if not week_existing:
                return JsonResponse('Error', safe=False)

            summary_week_details = []
            color_list = ['#e0ffff', '#cefdce', '#ffffff']
            color_index = 0

            customers = Principal.objects.all().order_by('name')
            week_detail = SummaryWeek.objects.filter(Q(year__year_label=year) & Q(week=week))
            week_serializer = SummaryWeekSerializer(week_detail, many=True)
            details['week'] = week_serializer.data

            for customer in customers:
                data = {}
                total = []
                data['customer'] = customer.name
                data['color'] = color_list[color_index % 3]
                color_index += 1
                sub_customers = CustomerCustom.objects.filter(Q(customer__name=customer.name)).order_by('customer__name','sub_customer')
                if sub_customers:
                    customer_total = 0
                    last_index = 0
                    for sub_customer in sub_customers:
                        data = copy.deepcopy(data)
                        data['sub_customer'] = sub_customer.sub_customer
                        summary_customer = SummaryCustomer.objects.filter(Q(week=week_detail[0]) & Q(customer_custom=sub_customer))
                        if summary_customer:
                            customer = summary_customer[0]
                            data['id'] = customer.pk
                            data['date_billing'] = customer.date_billing
                            data['date_end'] = customer.date_end
                            data['detail'] = customer.detail

                            week_total = Invoice.objects.filter(Q(customer_week = customer)).annotate(sum_drayage_total=Sum('drayage_total'), sum_gate_total=Sum('gate_total')).values_list('sum_drayage_total', 'sum_gate_total')
                            if week_total:
                                
                                drayage_total, gate_total = zip(*week_total)
                                data['drayage_total'] = float(drayage_total[0])
                                data['gate_total'] = float(gate_total[0])
                                customer_total += data['drayage_total']

                            if last_index == len(sub_customers)-1 and len(sub_customers) > 1:
                                data['cusotomer_total'] = customer_total
                                customer_total = 0
                                last_index = 0
                            
                            last_index += 1

                        summary_week_details.append(data)
                else:
                    summary_customer = SummaryCustomer.objects.filter(Q(week=week_detail[0]) & Q(customer_main=customer))
                    if summary_customer:
                        customer = summary_customer[0]
                        data['id'] = customer.pk
                        data['date_billing'] = customer.date_billing
                        data['date_end'] = customer.date_end
                        data['detail'] = customer.detail

                        week_total = Invoice.objects.filter(Q(customer_week = customer)).annotate(sum_drayage_total=Sum('drayage_total'), sum_gate_total=Sum('gate_total')).values_list('sum_drayage_total', 'sum_gate_total')

                        if week_total:
                            drayage_total, gate_total = zip(*week_total)
                            data['drayage_total'] = float(drayage_total[0])
                            data['gate_total'] = float(gate_total[0])
 
                    summary_week_details.append(data)
            details['summary_week_details'] = summary_week_details            
            return JsonResponse(details, safe=False)
    return JsonResponse('Error', safe=False)
