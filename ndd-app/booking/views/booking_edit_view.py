# -*- coding: utf-8 -*-

import re
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from .booking_page_view import api_filter_bookings


@csrf_exempt
def api_save_edit_bookings(request):
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
            if booking['yard_ndd'] == '1':
                forward_tr = booking['forward_tr']
                backward_tr = forward_tr
                return_tr = forward_tr
            if booking['nextday'] == '1':
                backward_tr = booking['backward_tr']
                return_tr = backward_tr
            if booking['fac_ndd'] == '1':
                return_tr = booking['return_tr']

            booking_save = Booking.objects.get(pk=booking['id'])
            booking_save.status = booking['status']
            booking_save.time = booking['time']
            booking_save.date = booking['date']
            booking_save.agent = re.sub(' +', ' ', booking['agent'].strip().upper())
            booking_save.size = re.sub(' +', ' ', booking['size'].strip())
            booking_save.booking_no = re.sub(' +', ' ', booking['booking_no'].strip())
            booking_save.start = re.sub(' +', ' ', booking['start'].strip().upper())
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
            if booking['nextday'] == '1':
                booking_save.return_date = booking['return_date']
            else:
                booking_save.pickup_date = booking['date']
                booking_save.factory_date = booking['date']
                booking_save.return_date = booking['date']
            booking_save.vessel = re.sub(' +', ' ', booking['vessel'].strip())
            booking_save.port = re.sub(' +', ' ', booking['port'].strip())
            booking_save.save()

    return api_filter_bookings(request)
