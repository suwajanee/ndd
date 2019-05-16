# -*- coding: utf-8 -*-

import re
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from .booking_add_view import run_work_id
from .booking_page_view import api_filter_bookings
from .utility.functions import check_key_detail
from customer.models import Shipper


@csrf_exempt
def api_save_edit_bookings(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            bookings = req['bookings']

            for booking in bookings:
                if not booking['date']:
                    booking['date'] = None
                if not booking['closing_date']:
                    booking['closing_date'] = None
                if not booking['return_date']:
                    booking['return_date'] = None
                
                pickup_tr = booking['pickup_tr']
                forward_tr = pickup_tr
                backward_tr = pickup_tr
                return_tr = pickup_tr
                if booking['yard_ndd'] == '1' or booking['yard_ndd'] == '2':
                    forward_tr = booking['forward_tr']
                    backward_tr = forward_tr
                    return_tr = forward_tr
                if booking['nextday'] == '1':
                    backward_tr = booking['backward_tr']
                    return_tr = backward_tr
                if booking['fac_ndd'] == '1' or booking['fac_ndd'] == '3':
                    return_tr = booking['return_tr']
                elif booking['fac_ndd'] == '2':
                    backward_tr = booking['backward_tr']
                    return_tr = booking['return_tr']

                booking_save = Booking.objects.get(pk=booking['id'])

                if str(booking_save.date) != booking['date']:
                    work_id, work_number = run_work_id(booking['date'])
                    booking_save.work_id = work_id
                    booking_save.work_number = work_number

                booking_save.status = booking['status']
                booking_save.time = booking['time']
                booking_save.date = booking['date']
                if booking['shipper']:
                    booking_save.shipper = Shipper.objects.get(pk=booking['shipper']['id'])
                booking_save.agent = re.sub(' +', ' ', booking['agent'].strip().upper())
                booking_save.size = re.sub(' +', ' ', booking['size'].strip())
                booking_save.booking_no = re.sub(' +', ' ', booking['booking_no'].strip())
                booking_save.pickup_tr = re.sub(' +', ' ', pickup_tr.strip())
                booking_save.pickup_from = re.sub(' +', ' ', booking['pickup_from'].strip().upper())
                booking_save.yard_ndd = booking['yard_ndd']
                booking_save.forward_tr = re.sub(' +', ' ', forward_tr.strip())
                booking_save.factory = re.sub(' +', ' ', booking['factory'].strip().upper())
                booking_save.backward_tr = re.sub(' +', ' ', backward_tr.strip())
                booking_save.fac_ndd = booking['fac_ndd']
                booking_save.return_tr = re.sub(' +', ' ', return_tr.strip())
                booking_save.return_to = re.sub(' +', ' ', booking['return_to'].strip().upper())
                booking_save.container_no = re.sub(' +', ' ', booking['container_no'].strip())
                booking_save.seal_no = re.sub(' +', ' ', booking['seal_no'].strip())
                booking_save.tare = re.sub(' +', ' ', booking['tare'].strip())
                booking_save.closing_date = booking['closing_date']
                booking_save.closing_time = booking['closing_time']
                booking_save.remark = re.sub(' +', ' ', booking['remark'].strip())
                booking_save.nextday = booking['nextday']
                if booking['nextday'] == '1' or booking['nextday'] == '2':
                    booking_save.return_date = booking['return_date']
                    booking_save.detail = {}
                    booking_save.detail = check_key_detail(booking_save.detail, booking['detail'], 'return_time', True)
                    
                else:
                    booking_save.pickup_date = booking['date']
                    booking_save.factory_date = booking['date']
                    booking_save.return_date = booking['date']
                    try:
                        booking_save.detail.pop('return_time')
                    except:
                        pass

                booking_save.vessel = re.sub(' +', ' ', booking['vessel'].strip())
                booking_save.port = re.sub(' +', ' ', booking['port'].strip())
                booking_save.save()

        return api_filter_bookings(request)
    return JsonResponse('Error', safe=False)          

@csrf_exempt
def api_change_state_booking(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            
            booking_id = req['booking_id']
            state = req['state']

            booking = Booking.objects.get(pk=booking_id)
            if booking.status == '3' and state == '3':
                state = '1'
            booking.status = state
            booking.save()

            return JsonResponse(booking.status, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_change_color_field(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            
            booking_id = req['id']
            field = req['field']
            color = {field: req['color']}

            booking = Booking.objects.get(pk=booking_id)
            if not booking.detail:
                booking.detail = {}
            booking.detail = check_key_detail(booking.detail, color, field, True)
            booking.save()

            if field in booking.detail:
                color_key = booking.detail[field]
            else:
                color_key = 0

            return JsonResponse(color_key, safe=False)
    return JsonResponse('Error', safe=False)