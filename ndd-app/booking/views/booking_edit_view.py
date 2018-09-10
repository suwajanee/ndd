# -*- coding: utf-8 -*-

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
    def render_edit_booking_page(request):
        template_name = 'booking/booking_edit.html'

        tmr = datetime.now() + timedelta(days=1)
        today = datetime.now()

        if request.method == "GET":
            filter_by = request.GET.get("filter_by")
            date_filter = request.GET.get("date_filter")

            if date_filter == None:
                date_filter = ''

            if not date_filter:
                bookings = Booking.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
            else:
                if filter_by == "month":
                    month_of_year = datetime.strptime(date_filter, '%Y-%m')
                    bookings = Booking.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | ((Q(closing_date__lte=tmr) | Q(date__lte=today)) & (Q(return_tr='') & Q(cancel=0)))).order_by('date', 'work_id')
                else:
                    bookings = Booking.objects.filter(Q(date=date_filter) | ((Q(closing_date__lte=tmr) | Q(date__lte=today)) & (Q(return_tr='') & Q(cancel=0)))).order_by('date', 'work_id')

        else:
            bookings = Booking.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')

        return render(request, template_name, {'bookings': bookings, 'filter_by': filter_by, 'date_filter': date_filter, 'today': today, 'tmr': tmr, 'nbar': 'booking-table'})

    @login_required(login_url=reverse_lazy('login'))
    def save_edit_data_booking(request):
        if request.method == 'POST':
            pk = request.POST.getlist('pk')
            time = request.POST.getlist('time')
            date = request.POST.getlist('date')
            size = request.POST.getlist('size')
            booking_no = request.POST.getlist('booking_no')
            pickup_tr = request.POST.getlist('pickup_tr')
            pickup_from = request.POST.getlist('pickup_from')
            forward_tr = request.POST.getlist('forward_tr')
            factory = request.POST.getlist('factory')
            backward_tr = request.POST.getlist('backward_tr')
            return_tr = request.POST.getlist('return_tr')
            return_to = request.POST.getlist('return_to')
            container_no = request.POST.getlist('container_no')
            seal_no = request.POST.getlist('seal_no')
            closing_date = request.POST.getlist('closing_date')
            closing_time = request.POST.getlist('closing_time')
            ref = request.POST.getlist('ref')
            remark = request.POST.getlist('remark')
            return_date = request.POST.getlist('return_date')

            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            for i in range(len(pk)):
                if not date[i]:
                    date[i] = None
                if not closing_date[i]:
                    closing_date[i] = None
                if not return_date[i]:
                    return_date[i] = None

                booking = Booking.objects.get(pk=pk[i])
                booking.time = time[i]
                booking.date = date[i]
                booking.size = size[i]
                booking.booking_no = booking_no[i]
                booking.pickup_tr = pickup_tr[i]
                booking.pickup_from = pickup_from[i]
                booking.forward_tr = forward_tr[i]
                booking.factory = factory[i]
                booking.backward_tr = backward_tr[i]
                booking.return_tr = return_tr[i]
                booking.return_to = return_to[i]
                booking.container_no = container_no[i]
                booking.seal_no = seal_no[i]
                booking.closing_date = closing_date[i]
                booking.closing_time = closing_time[i]
                booking.ref = ref[i]
                booking.remark = remark[i]
                booking.pickup_date = date[i]
                booking.factory_date = date[i]
                booking.return_date = return_date[i]
                booking.save()

            messages.success(request, "Saving Booking.")
            return redirect(reverse('booking-edit') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)
        else:
            return redirect('booking-edit')
