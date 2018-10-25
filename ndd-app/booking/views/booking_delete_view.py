# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Booking
from .booking_page_view import api_filter_bookings


@csrf_exempt
def api_delete_bookings(request):
    if request.method == "POST":
        req = json.loads( request.body.decode('utf-8') )
        pk_list = req["checked_bookings"]
        print(pk_list)

        for pk in pk_list:
            booking = Booking.objects.get(pk=pk)
            booking.delete()

    return api_filter_bookings(request)
