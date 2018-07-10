from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from ..models import Booking
from ..forms import BookingFilterForm

class BookingTableView(TemplateView):
    
    def get_table(request):
        template_name = 'table.html'
        if request.method == "POST":
            form = BookingFilterForm(request.POST)
            date = request.POST.get("date")
            bookings = Booking.objects.filter(date=date).order_by('work_id')
        else:
            form = BookingFilterForm()
            bookings = Booking.objects.order_by('work_id')
        return render(request, template_name, {'bookings': bookings, 'form' : form})
