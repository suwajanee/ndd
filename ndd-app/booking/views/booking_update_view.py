from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper

from datetime import datetime, timedelta, date
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class BookingUpdateView(TemplateView):
    @login_required(login_url=reverse_lazy('login'))
    def update_data_booking(request):
        if request.method == 'POST':
            pk = request.POST['pk']
            vessel = request.POST['vessel']
            port = request.POST['port']
            
            address = request.POST['address'+pk]
            if address == 'other':
                address_other = request.POST['address_other']

            cancel = request.POST['cancel']

            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            booking = Booking.objects.get(pk=pk)
            booking.vessel = vessel
            booking.port = port
            booking.address = address
            if address == 'other':
                booking.address_other = address_other
            booking.cancel = cancel
            booking.save()

            messages.success(request, "Updated Booking.")
            return redirect(reverse('booking-table') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)
        else:
            return redirect('booking-table')