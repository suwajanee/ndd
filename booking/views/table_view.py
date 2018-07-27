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
        if request.method == "POST":
            form = BookingFilterSortForm(request.POST)
            date = request.POST.get("date")
            sort = request.POST.get("sort")

            if not date and  not sort:
                bookings = Booking.objects.order_by('work_id')
            elif not date:
                bookings = Booking.objects.order_by('date', sort)
            elif not sort:
                bookings = Booking.objects.filter(date=date).order_by('work_id')
            else:
                bookings = Booking.objects.filter(date=date).order_by('date', sort)

            request.session['form'] = request.POST
            request.session['date'] = date
            request.session['sort'] = sort
        else:
            form = BookingFilterSortForm()
            bookings = Booking.objects.order_by('work_id')

            if request.session.has_key('form'):
                form = BookingFilterSortForm(request.session['form'])
            if request.session.has_key('date'):
                date = request.session['date']
            if request.session.has_key('sort'):
                sort = request.session['sort']

            if not date and not sort:
                bookings = Booking.objects.order_by('work_id')
            elif not date:
                bookings = Booking.objects.order_by('date', sort)
            elif not sort:
                bookings = Booking.objects.filter(date=date).order_by('work_id')
            else:
                bookings = Booking.objects.filter(date=date).order_by('date', sort)

        return render(request, template_name, {'bookings': bookings, 'form' : form})

    def delete_data(request, pk):
        booking = Booking.objects.get(pk = pk)
        booking.delete()
        return redirect('booking-table')