# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from ..serializers import BookingSerializer


@login_required(login_url=reverse_lazy('login'))
def booking_page(request):
    return render(request, 'booking/booking_page.html', {'nbar': 'booking-page'})

@csrf_exempt
def api_get_bookings(request):
    if request.user.is_authenticated:
        context = {}
        context['tmr'] = datetime.now() + timedelta(days=1)
        context['today'] = datetime.now()

        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            filter_by = req['filter_by']
            date_filter = req['date_filter']
            if date_filter == '':
                date_filter = None

            if date_filter == None:
                bookings = Booking.objects.filter(Q(date=context['today']) | Q(status__in=[1,3,4,5])).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')
            elif filter_by == "month":
                month_of_year = datetime.strptime(date_filter, '%Y-%m')
                bookings = Booking.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | ((Q(closing_date__lte=context['tmr']) | Q(date__lte=context['today'])) & Q(status__in=[1,3,4,5]))).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')
            else:
                bookings = Booking.objects.filter(Q(date=date_filter) | ((Q(closing_date__lte=context['tmr']) | Q(date__lte=context['today'])) & Q(status__in=[1,3,4,5]))).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')

        else:
            bookings = Booking.objects.filter(Q(date=context['today']) | Q(status__in=[1,3,4,5])).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')

        serializer = BookingSerializer(bookings, many=True)
        context['bookings'] = serializer.data
        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_filter_bookings(request):
    if request.user.is_authenticated:
        context = {}
        context['tmr'] = datetime.now() + timedelta(days=1)
        context['today'] = datetime.now()

        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            filter_data = req['filter_data']

            filter_dict = {}

            set_if_not_none(filter_dict, 'principal__pk', filter_data['principal_id'])
            set_if_not_none(filter_dict, 'shipper__pk', filter_data['shipper'])
            set_if_not_none(filter_dict, 'booking_no', filter_data['booking_no'])
            set_if_not_none(filter_dict, 'remark__contains', filter_data['remark'])
            set_if_not_none(filter_dict, 'date__gte', filter_data['date_from'])
            set_if_not_none(filter_dict, 'date__lte', filter_data['date_to'])

            bookings = Booking.objects.filter(**filter_dict).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')

        else:
            return api_get_bookings(request)
            
        serializer = BookingSerializer(bookings, many=True)
        context['bookings'] = serializer.data

        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)            

def set_if_not_none(mapping, key, value):
    if value is not None and value:
        mapping[key] = value