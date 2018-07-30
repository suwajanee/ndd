from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from customer.models import Principal, Shipper
from ..forms import BookingFilterSortForm
# from django.shortcuts import render_to_response
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
import requests

class BookingTableView(TemplateView):
    
    def get_table(request):
        template_name = 'table.html'
        if request.method == "GET":
            form = BookingFilterSortForm(request.GET)
            date = request.GET.get("date")

            if date == None:
                date = ''

            if not date:
                bookings = Booking.objects.order_by('work_id')
            else:
                bookings = Booking.objects.filter(date=date).order_by('work_id')

        return render(request, template_name, {'bookings': bookings, 'form': form, 'date': date})

    def delete_data(request, pk):
        booking = Booking.objects.get(pk=pk)
        booking.delete()

        if request.method == "GET":
            date = request.GET.get("date")
            if not date:
                return redirect(reverse('booking-table'))
            else:
                return redirect(reverse('booking-table') + '?date=' + date)