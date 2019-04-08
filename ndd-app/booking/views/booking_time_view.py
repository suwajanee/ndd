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

        booking_time = BookingTime.objects.filter(booking__pk__in=pk_list).order_by('booking__date', 'booking__principal__name', 'booking__shipper__name', 'booking__booking_no', 'booking__work_id')
        serializer_time = BookingTimeSerializer(booking_time, many=True)
        context['booking_time'] = serializer_time.data

        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)                  

@csrf_exempt
def api_save_time_bookings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            bookings = req['bookings']

            for booking in bookings:
                booking_time = booking['booking_time']

                pickup_in = booking_time['pickup_in_time']
                pickup_out = booking_time['pickup_out_time']
                factory_in = booking_time['factory_in_time']
                factory_load_start = booking_time['factory_load_start_time']
                factory_load_finish = booking_time['factory_load_finish_time']
                factory_out = booking_time['factory_out_time']
                return_in = booking_time['return_in_time']
                return_out = booking_time['return_out_time']

                try:
                    booking_time = BookingTime.objects.filter(booking__pk=booking['id'])
                except:
                    booking_time = None

                time_update = pickup_in['time'] or pickup_out['time'] or factory_in['time'] or factory_load_start['time'] or factory_load_finish['time'] or \
                        factory_out['time'] or return_in['time'] or return_out['time']

                if time_update:
                    data = {
                        'booking': Booking.objects.get(pk=booking['id']),
                        'pickup_in_time': pickup_in,
                        'pickup_out_time': pickup_out,
                        'factory_in_time': factory_in,
                        'factory_load_start_time': factory_load_start,
                        'factory_load_finish_time': factory_load_finish,
                        'factory_out_time': factory_out,
                        'return_in_time': return_in,
                        'return_out_time': return_out,
                    }
                    if booking_time:
                        time = booking_time.update(**data)
                    else:
                        time = BookingTime(**data)
                        time.save()
                else:
                    if booking_time:
                        booking_time.delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)                  
