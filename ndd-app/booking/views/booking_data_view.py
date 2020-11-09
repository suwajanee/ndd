# -*- coding: utf-8 -*-

from datetime import datetime
import re
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking, ContainerSize
from ..serializers import BookingSerializer, ContainerSizeSerializer
from summary.views.summary_week_view import get_week_details


@csrf_exempt
def api_check_work_id(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            work_id = req['work_id']
            try:
                bookings = Booking.objects.get(work_id=work_id.strip())                
                return JsonResponse('Existing', safe=False)
            except:
                return JsonResponse('Error', safe=False)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_work_list(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            week = req['week']
            year = req['year']
            customer = req['customer']

            today = datetime.today()

            week, week_serializer = get_week_details(week, year)

            bookings = Booking.objects.filter(Q(principal__pk=customer) & ~Q(status=0) & ((Q(date__lte=today) & Q(date__gte=week.date_start)) | \
                        (Q(date__lte=week.date_end) & ~Q(summary_status='1')))).order_by('date', 'shipper__name', 'booking_no', 'work_id')

            serializer = BookingSerializer(bookings, many=True)
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
        booking_save.seal_no = re.sub(' +', ' ', booking['seal_no'].strip())
        booking_save.size = re.sub(' +', ' ', booking['size'].strip())
        booking_save.agent = re.sub(' +', ' ', booking['agent'].strip())
        booking_save.save()

    return True

@csrf_exempt
def api_get_booking_daily_works(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            data = {}
            today = datetime.today()

            data['cancel'] = Booking.objects.filter(Q(date=today) & Q(status=0)).count()
            data['not_start'] = not_start = Booking.objects.filter(Q(date=today) & Q(status=1)).count()
            data['pending'] = pending = Booking.objects.filter(Q(date=today) & Q(status__in=[3,4,5])).count()
            data['completed'] = completed = Booking.objects.filter(Q(date=today) & Q(status=2)).count()
            data['total'] = not_start + pending + completed

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_container_size(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            data = {}
            
            container_1 = ContainerSize.objects.filter(num=1).order_by('size')
            container_2 = ContainerSize.objects.filter(num=2).order_by('size')

            serializer_1 = ContainerSizeSerializer(container_1, many=True)
            serializer_2 = ContainerSizeSerializer(container_2, many=True)

            data['num_1'] = serializer_1.data
            data['num_2'] = serializer_2.data

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_normal_work_by_work_id(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            work_id = req['work_id']

            try:
                work = Booking.objects.get(work_id=work_id)
                serializer = BookingSerializer(work, many=False)
                data = serializer.data
            except Booking.DoesNotExist:
                data = None

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)
