# -*- coding: utf-8 -*-

import copy
import json

from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Year, CustomerCustom, SummaryWeek, Invoice
from customer.models import Principal
from ..serializers import YearSerializer


@csrf_exempt
def api_get_summary_year(request):
    if request.user.is_authenticated:
        summary_year = []
        if request.method == "POST":
            years = Year.objects.all().order_by('-year_label')
            for year in years:
                data = {}
                data['year'] = year.year_label
                year_total = Invoice.objects.filter(customer_week__week__year=year).aggregate(total=Sum('drayage_total') + Sum('gate_total'))['total']
                data['total'] = year_total

                summary_week = SummaryWeek.objects.filter(year=year).values_list('status', flat=True).distinct()
                if '0' in summary_week:
                    data['status'] = 'alert-warning'
                elif '1' in summary_week:
                    data['status'] = 'alert-success'
                else:
                    data['status'] = 'alert-dark'
                summary_year.append(data)

            return JsonResponse(summary_year, safe=False)
        else:
            years = Year.objects.all().order_by('-year_label')
            serializer = YearSerializer(years, many=True)

            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_year(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            data = req['year']
            year_existing = Year.objects.filter(year_label=data['year_label'])
            if not year_existing:
                year = Year(**data)
                year.save()
            
            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_summary_year_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']

            year_existing = Year.objects.filter(year_label=year)
            if not year_existing:
                return JsonResponse('Error', safe=False)

            summary_year_details = []
            color_list = ['#e0ffff', '#cefdce', '#ffffff']
            color_index = 0

            customers = Principal.objects.all().order_by('name')
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
                        total = []
                        for month in range(0,12):
                            month = str(month+1)
                            month_total = Invoice.objects.filter(Q(customer_week__week__year__year_label=year) & Q(customer_week__week__month=month) & \
                                            Q(customer_week__customer_custom = sub_customer) & \
                                            Q(customer_week__customer_custom__sub_customer = sub_customer.sub_customer)).aggregate(total=Sum('drayage_total') + Sum('gate_total'))['total']

                            if month_total:
                                total.append(float(month_total))
                                customer_total += float(month_total)
                            else:
                                total.append(None)

                            data['total'] = total

                        if last_index == len(sub_customers)-1:
                            data['cusotomer_total'] = customer_total
                            customer_total = 0
                            last_index = 0
                        
                        last_index += 1

                        summary_year_details.append(data)
                else:
                    for month in range(0,12):
                        month = str(month+1)
                        month_total = Invoice.objects.filter(Q(customer_week__week__year__year_label=year) & Q(customer_week__week__month=month) & \
                                        Q(customer_week__customer_main__name = customer.name)).aggregate(total=Sum('drayage_total') + Sum('gate_total'))['total']
                        if month_total:
                            total.append(float(month_total))
                        else:
                            total.append(None)

                        data['total'] = total
                    summary_year_details.append(data)
            return JsonResponse(summary_year_details, safe=False)
    return JsonResponse('Error', safe=False)
