# -*- coding: utf-8 -*-

from datetime import datetime
import json
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from ..serializers import BookingSerializer
from customer.models import Principal, Shipper


@login_required(login_url=reverse_lazy('login-page'))
def booking_add_page(request):
    return render(request, 'booking/booking_add_page.html', {'nbar': 'booking-page'})

@csrf_exempt
def api_save_add_bookings(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )

        bookings = req['bookings']
        details = req['details']
        import_work = req['import']

        return_date = bookings['return_date']

        bookings['principal'] = Principal.objects.get(pk=bookings['principal'])
        bookings['shipper'] = Shipper.objects.get(pk=bookings['shipper'])
        bookings['agent'] = re.sub(' +', ' ', bookings['agent'].strip().upper())
        bookings['booking_no'] = re.sub(' +', ' ', bookings['booking_no'].strip())

        bookings['pickup_from'] = re.sub(' +', ' ', bookings['pickup_from'].strip().upper())
        bookings['factory'] = re.sub(' +', ' ', bookings['factory'].strip().upper())
        bookings['return_to'] = re.sub(' +', ' ', bookings['return_to'].strip().upper())

        bookings['vessel'] = re.sub(' +', ' ', bookings['vessel'].strip())
        bookings['port'] = re.sub(' +', ' ', bookings['port'].strip())

        if not bookings['closing_date']:
            bookings['closing_date'] = None
        bookings['closing_time'] = bookings['closing_time']

        bookings['remark'] = re.sub(' +', ' ', bookings['remark'].strip())

        if bookings['nextday'] == True:
            bookings['nextday'] = '1'
        else:
            bookings['nextday'] = '0'
        
        for detail in details:
            bookings['date'] = detail['date']
            bookings['pickup_date'] = detail['date']
            bookings['factory_date'] = detail['date']

            bookings['time'] = detail['time']
            bookings['size'] = detail['size']
            if import_work == True:
                bookings['container_no'] = detail['container_no']
                bookings['seal_no'] = detail['seal_no']

            if bookings['nextday'] == '1':
                if not return_date:
                    bookings['return_date'] = detail['date']
            else:
                bookings['return_date'] = detail['date']

            for i in range(int(detail['quantity'])):
                work_id, work_number = run_work_id(detail['date'])

                bookings['work_id'] = work_id
                bookings['work_number'] = work_number

                booking = Booking(**bookings)
                booking.save()

    return JsonResponse('Success', safe=False)

def run_work_id(date):
    work = Booking.objects.filter(date=date).aggregate(Max('work_number'))
    if work['work_number__max'] == None:
        work_number = 1
    else:
        work_number = work['work_number__max'] + 1

    work = str("{:03d}".format(work_number))
    date = datetime.strptime(date, "%Y-%m-%d")
    work_id = date.strftime('%d%m%y') + work

    while True:
        exist_id = Booking.objects.filter(work_id=work_id)
        if exist_id:
            work_number = work_number + 1
            work = str("{:03d}".format(work_number))
            work_id = date.strftime('%d%m%y') + work
        else:
            break

    return work_id, work_number
    