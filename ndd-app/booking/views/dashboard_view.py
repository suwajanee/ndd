# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from agent_transport.models import AgentTransport
from summary.models import Invoice


@login_required(login_url=reverse_lazy('login'))
def dashboard_page(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def api_get_weekly_works(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            
            today = datetime.today()
            before_1 = today - timedelta(days=1)
            before_2 = today - timedelta(days=2)
            before_3 = today - timedelta(days=3)
            after_1 = today + timedelta(days=1)
            after_2 = today + timedelta(days=2)
            after_3 = today + timedelta(days=3)

            booking_pending = []
            booking_completed = []
            agent_pending = []
            agent_completed = []
            for day in [before_3 ,before_2, before_1, today, after_1, after_2, after_3]:
                data1 = {}
                data2 = {}
                data3 = {}
                data4 = {}

                data1['x'] = data2['x'] = data3['x'] = data4['x'] = str(day.date()).split('-')
                data1['y'] = Booking.objects.filter(Q(date=day) & Q(status__in=[1, 3, 4, 5])).count()
                booking_pending.append(data1)

                data2['y'] = Booking.objects.filter(Q(date=day) & Q(status=2)).count()
                booking_completed.append(data2)

                data3['y'] = AgentTransport.objects.filter(Q(date=day) & Q(status__in=[1, 3, 4])).count()
                agent_pending.append(data3)

                data4['y'] = AgentTransport.objects.filter(Q(date=day) & Q(status=2)).count()
                agent_completed.append(data4)

            response = {
                'booking_pending': booking_pending,
                'booking_completed': booking_completed,
                'agent_pending': agent_pending,
                'agent_completed': agent_completed,
            }
            
            return JsonResponse(response, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_income(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            year = datetime.today().year

        elif request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']

        else:
            return JsonResponse('Error', safe=False)

        data = {}
        data['year'] = year

        total = []

        for month in range(0,12):
            month = str(month+1)
            month_total = Invoice.objects.filter(Q(customer_week__week__year__year_label=str(year)) & \
                            Q(customer_week__week__month=month)).aggregate(total=Sum('drayage_total'))['total']

            if month_total:
                total.append(month_total)
            else:
                total.append(0)

        data['total'] = total

        return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)