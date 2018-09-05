from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import Booking
from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class BookingTableView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def render_table_booking(request):
        template_name = 'booking/booking_table.html'

        tmr = datetime.now() + timedelta(days=1)
        today = datetime.now()

        if request.method == "GET":
            filter_by = request.GET.get("filter_by")
            date_filter = request.GET.get("date_filter")
            
            if date_filter == None:
                date_filter = ''

            if not date_filter:
                bookings = Booking.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
            else:
                if filter_by == "month":
                    month_of_year = datetime.strptime(date_filter, '%Y-%m')
                    bookings = Booking.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | ((Q(closing_date__lte=tmr) | Q(date__lte=today)) & (Q(return_tr='') & ~Q(cancel='1')))).order_by('date', 'work_id')
                else:
                    bookings = Booking.objects.filter(Q(date=date_filter) | ((Q(closing_date__lte=tmr) | Q(date__lte=today)) & (Q(return_tr='') & ~Q(cancel='1')))).order_by('date', 'work_id')

        else:
            bookings = Booking.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')

        return render(request, template_name, {'bookings': bookings, 'filter_by': filter_by, 'date_filter': date_filter, 'today': today, 'tmr': tmr, 'nbar': 'booking-table'})

