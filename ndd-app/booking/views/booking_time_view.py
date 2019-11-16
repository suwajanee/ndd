# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json
import re

from django.db.models import Q
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
                return JsonResponse('Error', safe=False)

        bookings = Booking.objects.filter(pk__in=pk_list).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')
        serializer_booking = BookingSerializer(bookings, many=True)
        context['bookings'] = serializer_booking.data

        booking_time = BookingTime.objects.filter(booking__pk__in=pk_list).order_by('booking__date', 'booking__principal__name', 'booking__shipper__name', 'booking__booking_no', 'booking__work_id', 'pk').distinct()
        serializer = BookingTimeSerializer(booking_time, many=True)
        context['booking_time'] = serializer.data

        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)                  

@csrf_exempt
def api_save_time_bookings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            bookings = req['bookings']

            for booking in bookings:

                pickup_time = booking['pickup_time']
                factory_time = booking['factory_time']
                return_time = booking['return_time']

                if pickup_time:
                    if not 'in' in pickup_time or not pickup_time['in']:
                        pickup_time.pop('in', None)
                    if not 'out' in pickup_time or not pickup_time['out']:
                        pickup_time.pop('out', None)
                
                if factory_time:
                    if not 'in' in factory_time or not factory_time['in']:
                        factory_time.pop('in', None)
                    if not 'start' in factory_time or not factory_time['start']:
                        factory_time.pop('start', None)
                    if not 'finish' in factory_time or not factory_time['finish']:
                        factory_time.pop('finish', None)
                    if not 'out' in factory_time or not factory_time['out']:
                        factory_time.pop('out', None)
                
                if return_time:
                    if not 'in' in return_time or not return_time['in']:
                        return_time.pop('in', None)
                    if not 'out' in return_time or not return_time['out']:
                        return_time.pop('out', None)

                booking_work = Booking.objects.get(pk=booking['id'])

                time_update = pickup_time or factory_time or return_time

                if time_update:
                    time_save, created = BookingTime.objects.update_or_create(
                        booking=booking_work,
                        defaults={'pickup_time': pickup_time, 'factory_time': factory_time, 'return_time': return_time},
                    )
                else:
                    BookingTime.objects.filter(booking=booking_work).delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)
