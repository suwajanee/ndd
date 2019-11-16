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

        booking_time = BookingTime.objects.filter(booking__pk__in=pk_list, key='').order_by('booking__date', 'booking__principal__name', 'booking__shipper__name', 'booking__booking_no', 'booking__work_id', 'pk').distinct()
        serializer = BookingTimeSerializer(booking_time, many=True)
        context['booking_time'] = serializer.data
        # bookings = Booking.objects.filter(pk__in=pk_list).order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')
        # serializer_booking = BookingSerializer(bookings, many=True)
        # context['bookings'] = serializer_booking.data

        # data_list = []
        # for booking in bookings:
        #     booking_time = BookingTime.objects.filter(booking=booking)

        #     data = {
        #         'booking': booking.pk,
        #         'booking_time': {},
        #     }
        #     key_array = ['pickup_in', 'pickup_out', 'factory_in', 'factory_load_start', 'factory_load_finish', 'factory_out', 'return_in', 'return_out']

        #     for key in key_array:
        #         try:
        #             data['booking_time'][key] = booking_time.get(key=key).time
        #         except:
        #             data['booking_time'][key] = ''

        #     data_list.append(data)

        # context['booking_time'] = data_list

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
                        booking=booking_work, key='',
                        defaults={'pickup_time': pickup_time, 'factory_time': factory_time, 'return_time': return_time},
                    )
                else:
                    BookingTime.objects.filter(booking=booking_work).delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)



@csrf_exempt
def api_time_new(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            bookings = BookingTime.objects.all().values_list('booking',flat = True).order_by('booking__date', 'booking__principal__name', 'booking__shipper__name', 'booking__booking_no', 'booking__work_id', 'pk').distinct()
            booking_list = list(dict.fromkeys(bookings))


            key_array = ['pickup_in', 'pickup_out', 'factory_in', 'factory_load_start', 'factory_load_finish', 'factory_out', 'return_in', 'return_out']

            for book in booking_list:
                
                booking = Booking.objects.get(pk=book)
                booking_time = BookingTime.objects.filter(booking__pk=book)

                _pickup = booking_time.filter(key__contains='pickup')
                _factory = booking_time.filter(key__contains='factory')
                _return = booking_time.filter(key__contains='return')

                pickup_time = {}
                factory_time = {}
                return_time = {}

                if _pickup:
                    pickup_in = _pickup.filter(key='pickup_in').first()
                    pickup_out = _pickup.filter(key='pickup_out').first()

                    if pickup_in:
                        pickup_time['in'] = pickup_in.time
                    if pickup_out:
                        pickup_time['out'] = pickup_out.time

                if _factory:
                    factory_in = _factory.filter(key='factory_in').first()
                    factory_load_start = _factory.filter(key='factory_load_start').first()
                    factory_load_finish = _factory.filter(key='factory_load_finish').first()
                    factory_out = _factory.filter(key='factory_out').first()

                    if factory_in:
                        factory_time['in'] = factory_in.time
                    if factory_load_start:
                        factory_time['start'] = factory_load_start.time
                    if factory_load_finish:
                        factory_time['finish'] = factory_load_finish.time
                    if factory_out:
                        factory_time['out'] = factory_out.time

                if _return:
                    return_in = _return.filter(key='return_in').first()
                    return_out = _return.filter(key='return_out').first()

                    if return_in:
                        return_time['in'] = return_in.time
                    if return_out:
                        return_time['out'] = return_out.time


                data = {
                    'booking': booking,
                    'pickup_time': pickup_time,
                    'factory_time': factory_time,
                    'return_time': return_time
                }

                add_booking_time = BookingTime(**data)
                add_booking_time.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_remove_data(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            booking = BookingTime.objects.filter(~Q(key='')).delete()
            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)