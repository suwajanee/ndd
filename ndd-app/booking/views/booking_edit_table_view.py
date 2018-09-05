from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import Booking


class BookingEditTableView(TemplateView):
    
    @login_required(login_url=reverse_lazy('login'))
    def render_edit_booking(request):
        template_name = 'booking/booking_edit_table.html'

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


    @login_required(login_url=reverse_lazy('login'))
    def save_edit_data_booking(request):
        if request.method == 'POST':
            pk = request.POST['pk']
            time = request.POST['time']
            date = request.POST['date']
            size = request.POST['size']
            booking_no = request.POST['booking_no']
            pickup_tr = request.POST['pickup_tr']
            pickup_from = request.POST['pickup_from']
            forward_tr = request.POST['forward_tr']
            factory = request.POST['factory']
            backward_tr = request.POST['backward_tr']
            return_tr = request.POST['return_tr']
            return_to = request.POST['return_to']
            container_no = request.POST['container_no']
            seal_no = request.POST['seal_no']
            closing_date = request.POST['closing_date']
            closing_time = request.POST['closing_time']
            ref = request.POST['ref']
            remark = request.POST['remark']
            return_date = request.POST['return_date']

            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            if not date:
                date = None
            if not closing_date:
                closing_date = None
            if not return_date:
                return_date = None

            booking = Booking.objects.get(pk=pk)
            booking.time = time
            booking.date = date
            booking.size = size
            booking.booking_no = booking_no
            booking.pickup_tr = pickup_tr
            booking.pickup_from = pickup_from
            booking.forward_tr = forward_tr
            booking.factory = factory
            booking.backward_tr = backward_tr
            booking.return_tr = return_tr
            booking.return_to = return_to
            booking.container_no = container_no
            booking.seal_no = seal_no
            booking.closing_date = closing_date
            booking.closing_time = closing_time
            booking.ref = ref
            booking.remark = remark
            booking.pickup_date = date
            booking.factory_date = date
            booking.return_date = return_date
            booking.save()

            messages.success(request, "Saving Booking.")
            return redirect(reverse('booking-edit') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)
        else:
            return redirect('booking-edit')
