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
        delete_booking = BookingTableView()
        booking = Booking.objects.get(pk=pk)
        booking.delete()

        delete_booking.work_id_after_delete(booking)

        if request.method == "GET":
            date = request.GET.get("date")
            if not date:
                return redirect(reverse('booking-table'))
            else:
                return redirect(reverse('booking-table') + '?date=' + date)
    
    def work_id_after_delete(self, booking):
        date = booking.date
        re_work_id = Booking.objects.filter(date=date, work_number__gt=booking.work_number)
        if re_work_id:
            for work in re_work_id:               
                new_work_number = work.work_number - 1
                work_str = str("{:03d}".format(new_work_number))
                work_id = date.strftime('%d')+date.strftime('%m')+date.strftime('%y')+work_str

                booking = Booking.objects.get(pk=work.pk)
                booking.work_id = work_id
                booking.work_number = new_work_number
                booking.save()
        return None
