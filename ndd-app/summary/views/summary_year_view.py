# -*- coding: utf-8 -*-

# from datetime import datetime
import json
import re

from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Year, FormDetail, CustomerForm, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from ..serializers import YearSerializer
# from customer.models import Principal, Shipper


@csrf_exempt
def api_get_summary_year(request):
    summary_year = []
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        data = req['year']
    else:
        years = Year.objects.all().order_by('-name')
        for year in years:
            data = {}
            data['year'] = year.name
            year_total = Invoice.objects.filter(customer_week__week__year=year).aggregate(Sum('total'))['total__sum']
            data['total'] = year_total

            summary_week = set(SummaryWeek.objects.filter(year=year).values_list('status', flat=True))
            if '1' in summary_week:
                data['status'] = 'alert-warning'
            elif '2' in summary_week:
                data['status'] = 'alert-success'
            else:
                data['status'] = 'alert-dark'
            summary_year.append(data)

    return JsonResponse(summary_year, safe=False)

@csrf_exempt
def api_add_year(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        data = req['year']
        print(data)
        year = Year(**data)
        year.save()
        
        return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)