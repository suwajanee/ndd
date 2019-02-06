# -*- coding: utf-8 -*-

import re
import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from ..serializers import BookingSerializer
from summary.views.summary_week_view import get_week_details


@csrf_exempt
def api_get_work_list(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            week = req['week']
            year = req['year']
            customer = req['customer']

            week, week_serializer = get_week_details(week, year)

            bookings = Booking.objects.filter(Q(principal__pk=customer) & ~Q(status=0) & ((Q(date__lte=week.date_end) & Q(date__gte=week.date_start)) | \
                                            (Q(date__lte=week.date_end) & ~Q(summary_status='1')))).order_by('date', 'shipper__name', 'booking_no', 'work_id')

            serializer = BookingSerializer(bookings, many=True)
            # context['bookings'] = serializer.data
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

def booking_summary_status(work_id, status):
    bookings = Booking.objects.filter(pk__in=work_id).update(summary_status=status)
    return JsonResponse(True, safe=False)

def booking_edit_summary(bookings):
    for booking in bookings:
        booking_save = Booking.objects.get(pk=booking['id'])

        booking_save.booking_no = re.sub(' +', ' ', booking['booking_no'].strip())
        booking_save.pickup_from = re.sub(' +', ' ', booking['pickup_from'].strip())
        booking_save.return_to = re.sub(' +', ' ', booking['return_to'].strip())
        booking_save.container_no = re.sub(' +', ' ', booking['container_no'].strip())
        booking_save.size = re.sub(' +', ' ', booking['size'].strip())
        booking_save.save()

    return True
