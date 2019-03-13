# -*- coding: utf-8 -*-

import copy
import json

from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import CustomerCustom, Invoice, SummaryCustomer, SummaryWeek, Year
from ..serializers import CustomerCustomSerializer
from ..serializers import SummaryWeekSerializer
from customer.models import Principal
from customer.serializers import PrincipalSerializer


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
def api_get_diesel_rate(request):
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

            summary_week = SummaryWeek.objects.get(pk=data['id'])
            summary_week.year = Year.objects.get(year_label=data['year'])
            summary_week.month = data['month']
            summary_week.week = data['week']
            summary_week.date_start = data['date_start']
            summary_week.date_end = data['date_end']
            summary_week.diesel_rate = data['diesel_rate']

            summary_week.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_summary_week_status(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            week_id = req['id']
            week_status = req['status']

            summary_week = SummaryWeek.objects.get(pk=week_id)

            summary_week.status = week_status
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

            week_detail, details['week'] = get_week_details(week, year)

            if not week_detail:
                return JsonResponse('Error', safe=False)

            summary_week_details = []

            customers = Principal.objects.all().order_by('cancel', 'name')

            for customer in customers:
                data = {}
                total = []
                principal_serializer = PrincipalSerializer(customer, many=False)
                data['customer'] = principal_serializer.data

                sub_customers = CustomerCustom.objects.filter(Q(customer__name=customer.name)).order_by('customer__name','sub_customer')
                if sub_customers:
                    customer_total = 0
                    last_index = 0
                    for sub_customer in sub_customers:
                        data = copy.deepcopy(data)
                        customer_custom_serializer = CustomerCustomSerializer(sub_customer, many=False)
                        data['customer_custom'] = customer_custom_serializer.data
                        
                        summary_customer = SummaryCustomer.objects.filter(Q(week=week_detail) & Q(customer_custom=sub_customer))

                        if summary_customer:
                            data = summary_customer_json(data, summary_customer)
                        else:
                            data = summary_customer_json(data, '')

                        summary_week_details.append(data)
                else:
                    summary_customer = SummaryCustomer.objects.filter(Q(week=week_detail) & Q(customer_main=customer))
                    if summary_customer:
                        data = summary_customer_json(data, summary_customer)
 
                    summary_week_details.append(data)
            details['summary_week_details'] = summary_week_details            
            return JsonResponse(details, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_summary_weeks_by_year(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']

            week = SummaryWeek.objects.filter(Q(year__year_label=year))
            week_serializer = SummaryWeekSerializer(week, many=True)
            return JsonResponse(week_serializer.data, safe=False)
    return JsonResponse('Error', safe=False)


# Method
def summary_customer_json(data, summary_customer):
    if summary_customer:
        customer = summary_customer[0]
        data['id'] = customer.pk
        data['date_billing'] = customer.date_billing
        data['date_end'] = customer.date_end
        data['detail'] = customer.detail
        data['status'] = customer.status

        invoice = Invoice.objects.filter(Q(customer_week = customer))
        drayage_total = invoice.aggregate(sum_drayage_total=Sum('drayage_total'))['sum_drayage_total']
        gate_total = invoice.aggregate(sum_gate_total=Sum('gate_total'))['sum_gate_total']
        if drayage_total or gate_total:
            data['drayage_total'] = float(drayage_total)
            data['gate_total'] = float(gate_total)
    else:
        data['id'] = ''
        data['date_billing'] = ''
        data['date_end'] = ''
        data['detail'] = ''
        data['status'] = ''
        data['drayage_total'] = 0
        data['gate_total'] = 0

    return data

def get_week_details(week, year):
    try:
        week_detail = SummaryWeek.objects.get(Q(year__year_label=year) & Q(week=week))
    except:
        return False, False
    week_serializer = SummaryWeekSerializer(week_detail, many=False)

    return week_detail, week_serializer.data
