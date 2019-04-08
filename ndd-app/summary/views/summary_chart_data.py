# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Invoice, Year
from customer.models import Principal


@csrf_exempt
def api_summary_year_total_chart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']

            year_existing = Year.objects.filter(year_label=year)
            if not year_existing:
                return JsonResponse('Error', safe=False)

            summary_year_details = []

            customers = Principal.objects.all().order_by('-cancel', '-name')
            for customer in customers:
                data = {}
                data['customer'] = customer.name
                
                year_total = Invoice.objects.filter(Q(customer_week__week__year=year_existing[0]) & \
                                Q(customer_week__customer_main = customer)).aggregate(total=Sum('drayage_total'))['total']

                data['total'] = year_total
                summary_year_details.append(data)
            return JsonResponse(summary_year_details, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_summary_customer_total_chart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            customer_id = req['customer_id']

            year_existing = Year.objects.filter(year_label=year)
            if not year_existing:
                return JsonResponse('Error', safe=False)

            total = []

            for month in range(0,12):
                month = str(month+1)
                month_total = Invoice.objects.filter(Q(customer_week__week__year=year_existing[0]) & Q(customer_week__week__month=month) & \
                                Q(customer_week__customer_main__pk = customer_id)).aggregate(total=Sum('drayage_total'))['total']

                if month_total:
                    total.append(month_total)
                else:
                    total.append(0)

            return JsonResponse(total, safe=False)
    return JsonResponse('Error', safe=False)