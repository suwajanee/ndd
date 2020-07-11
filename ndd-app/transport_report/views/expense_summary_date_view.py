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
            year_date = ExpenseSummaryDate.objects.filter(year=year)

            summary_date_list = []

            for month in range(1, 13):
                month_date = year_date.filter(month=month).order_by('date')
                serializer = ExpenseSummaryDateSerializer(month_date, many=True)

                summary_date_list.append(serializer.data)

            return JsonResponse(summary_date_list, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_summary_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            year = req['year']
            month = req['month']
            date = req['date']

            data = {
                'year': Year.objects.get(year_label=year),
                'month': month + 1,
                'date': date
            }

            summary_date = ExpenseSummaryDate(**data)
            summary_date.save()

            return api_get_summary_date(request)
    return JsonResponse(False, safe=False)

@csrf_exempt
def api_edit_summary_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            pk = req['pk']
            date = req['date']

            summary_date = ExpenseSummaryDate.objects.get(pk=pk)
            summary_date.date = date
            summary_date.save()

            return api_get_summary_date(request)
    return JsonResponse(False, safe=False)

@csrf_exempt
def api_delete_summary_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            pk = req['pk']

            summary_date = ExpenseSummaryDate.objects.get(pk=pk).delete()

            return api_get_summary_date(request)
    return JsonResponse(False, safe=False)