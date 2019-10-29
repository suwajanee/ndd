# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from ..models import BookingTime
from ..serializers import BookingSerializer, BookingTimeSerializer


@csrf_exempt
def api_get_time_bookings(request):
    if request.user.is_authenticated:
        context = {}
        context['tmr'] = datetime.now() + timedelta(days=1)
        context['today'] = datetime.now()
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            pk_list = req["checked_bookings"]

            request.session['checked_bookings'] = pk_list
        else:
            if 'checked_bookings' in request.session:
                pk_list = request.session['checked_bookings']
                request.session['checked_bookings'] = pk_list
            else:
                return JsonResponse('Not found', safe=False)

        bookings = Booking.objects.filter(pk__in=pk_list).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')
        serializer_booking = BookingSerializer(bookings, many=True)
        context['bookings'] = serializer_booking.data

        data_list = []
        for booking in bookings:
            booking_time = BookingTime.objects.filter(booking=booking)

            data = {
                'booking': booking.pk,
                'booking_time': {},
            }
            key_array = ['pickup_in', 'pickup_out', 'factory_in', 'factory_load_start', 'factory_load_finish', 'factory_out', 'return_in', 'return_out']

            for key in key_array:
                try:
                    data['booking_time'][key] = booking_time.get(key=key).time
                except:
                    data['booking_time'][key] = ''

            data_list.append(data)

        context['booking_time'] = data_list

        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)                  

@csrf_exempt
def api_save_time_bookings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            bookings = req['bookings']

            for booking in bookings:
                time = booking['booking_time']

                pickup_in = time['pickup_in']
                pickup_out = time['pickup_out']
                factory_in = time['factory_in']
                factory_load_start = time['factory_load_start']
                factory_load_finish = time['factory_load_finish']
                factory_out = time['factory_out']
                return_in = time['return_in']
                return_out = time['return_out']

                booking_work = Booking.objects.get(pk=booking['id'])

                time_update = pickup_in or pickup_out or factory_in or factory_load_start or factory_load_finish or factory_out or return_in or return_out

                key_array = ['pickup_in', 'pickup_out', 'factory_in', 'factory_load_start', 'factory_load_finish', 'factory_out', 'return_in', 'return_out']

                if time_update:
                    for key in key_array:

                        if time[key]:
                            data = {
                                'booking': booking_work,
                                'key': key,
                                'time': time[key] 
                            }

                            time_save, created = BookingTime.objects.update_or_create(
                                booking=booking_work, key=key,
                                defaults={'time': time[key]},
                            )

                        else:
                            BookingTime.objects.filter(booking=booking_work, key=key).delete()

                else:
                    BookingTime.objects.filter(booking=booking_work).delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)     



@csrf_exempt
def api_add_time(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            bookings = BookingTime.objects.values_list('booking', 'pickup_in_time', 'pickup_out_time', 'factory_in_time', 'factory_load_start_time', 'factory_load_finish_time', 'factory_out_time', 'return_in_time', 'return_out_time').order_by('booking__date', 'booking__principal__name', 'booking__shipper__name', 'booking__booking_no', 'booking__work_id', 'pk')

            key_array = ['pickup_in', 'pickup_out', 'factory_in', 'factory_load_start', 'factory_load_finish', 'factory_out', 'return_in', 'return_out']

            for booking in bookings:
                print('11111111111111111111')
                work = Booking.objects.get(pk=booking[0])

                for item in range(1, len(booking)):

                    time = booking[item]['time']
                    if time:
                        data = {
                            'booking': work,
                            'key': key_array[item-1],
                            'time': time
                        }
                        print(data)

                        booking_save = BookingTime(**data)
                        booking_save.save()
            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_remove_data(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            bookings = BookingTime.objects.filter(key='').delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)