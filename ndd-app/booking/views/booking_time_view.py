# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from ..serializers import BookingSerializer


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

        bookings = Booking.objects.filter(pk__in=pk_list).order_by('date', 'principal__name', 'shipper__name', 'work_id')
        
        serializer = BookingSerializer(bookings, many=True)
        context['bookings'] = serializer.data

        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)                  

@csrf_exempt
def api_save_time_bookings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            bookings = req['bookings']

            for booking in bookings:
                booking_save = Booking.objects.get(pk=booking['id'])
                booking_save.pickup_in_time = booking['pickup_in_time__date'] + '//' + re.sub(' +', ' ', booking['pickup_in_time__time'].strip())
                booking_save.pickup_out_time = booking['pickup_out_time__date'] + '//' + re.sub(' +', ' ', booking['pickup_out_time__time'].strip())
                booking_save.factory_in_time = booking['factory_in_time__date'] + '//' + re.sub(' +', ' ', booking['factory_in_time__time'].strip())
                booking_save.factory_load_start_time = booking['factory_load_start_time__date'] + '//' + re.sub(' +', ' ', booking['factory_load_start_time__time'].strip())
                booking_save.factory_load_finish_time = booking['factory_load_finish_time__date'] + '//' + re.sub(' +', ' ', booking['factory_load_finish_time__time'].strip())
                booking_save.factory_out_time = booking['factory_out_time__date'] + '//' + re.sub(' +', ' ', booking['factory_out_time__time'].strip())
                booking_save.return_in_time = booking['return_in_time__date'] + '//' + re.sub(' +', ' ', booking['return_in_time__time'].strip())
                booking_save.return_out_time = booking['return_out_time__date'] + '//' + re.sub(' +', ' ', booking['return_out_time__time'].strip())
                
                booking_save.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)                  
