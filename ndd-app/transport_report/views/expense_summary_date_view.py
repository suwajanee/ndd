# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import ExpenseSummaryDate
from ..serializers import ExpenseSummaryDateSerializer
from summary.models import Year
from summary.serializers import YearSerializer


@login_required(login_url=reverse_lazy('login'))
def summary_date_page(request, year):
    try:
        year = Year.objects.get(year_label=year).year_label
    except:
        return HttpResponseRedirect('/dashboard')
    return render(request, 'summary_date_page.html', {'nbar': 'database-page', 'year': year})
    

@csrf_exempt
def api_get_summary_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            year_label = req['year']

            year = Year.objects.get(year_label=year_label)
            summary_date_list = ExpenseSummaryDate.objects.filter(year=year)


            ndd_summary = summary_date_list.filter(co='ndd')
            vts_summary = summary_date_list.filter(co='vts')

            ndd_list = []
            vts_list = []

            for month in range(1, 13):
                ndd = ndd_summary.filter(month=month).order_by('date')
                ndd_serializer = ExpenseSummaryDateSerializer(ndd, many=True)

                vts = vts_summary.filter(month=month).order_by('date')
                vts_serializer = ExpenseSummaryDateSerializer(vts, many=True)

                ndd_list.append(ndd_serializer.data)
                vts_list.append(vts_serializer.data)
            
            data = {
                'ndd': ndd_list,
                'vts': vts_list
            }
            
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_summary_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            year = req['year']
            month = req['month']
            co = req['co']
            date = req['date']

            data = {
                'year': Year.objects.get(year_label=year),
                'month': month + 1,
                'co': co,
                'date': date
            }

            summary_date = ExpenseSummaryDate(**data)
            summary_date.save()

            return api_get_summary_date(request)
    return JsonResponse(False, safe=False)
