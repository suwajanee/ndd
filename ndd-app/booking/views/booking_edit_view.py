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
        context = {}
        context['tmr'] = datetime.now() + timedelta(days=1)
        context['today'] = datetime.now()

        if request.method == "GET":
            
            context['filter_by'] = request.GET.get("filter_by")
            context['date_filter'] = request.GET.get("date_filter")
            context['nbar'] = 'booking-table'

            if context['date_filter'] == None:
                context['date_filter'] = ''

            if not context['date_filter']:
                context['bookings'] = Booking.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
            else:
                if context['filter_by']  == "month":
                    month_of_year = datetime.strptime(context['date_filter'], '%Y-%m')
                    context['bookings'] = Booking.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | ((Q(closing_date__lte=context['tmr']) | Q(date__lte=context['today'])) & (Q(return_tr='') & Q(cancel=0)))).order_by('date', 'work_id')
                else:
                    context['bookings'] = Booking.objects.filter(Q(date=context['date_filter']) | ((Q(closing_date__lte=context['tmr']) | Q(date__lte=context['today'])) & (Q(return_tr='') & Q(cancel=0)))).order_by('date', 'work_id')

        else:
           context['bookings'] = Booking.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')

        return render(request, template_name, context)        

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
                booking.size = size[i].strip()
                booking.booking_no = booking_no[i].strip()
                booking.pickup_tr = pickup_tr[i].strip()
                booking.pickup_from = pickup_from[i].strip()
                booking.forward_tr = forward_tr[i].strip()
                booking.factory = factory[i].strip()
                booking.backward_tr = backward_tr[i].strip()
                booking.return_tr = return_tr[i].strip()
                booking.return_to = return_to[i].strip()
                booking.container_no = container_no[i].strip()
                booking.seal_no = seal_no[i].strip()
                booking.closing_date = closing_date[i]
                booking.closing_time = closing_time[i]
                booking.ref = ref[i].strip()
                booking.remark = remark[i].strip()
                booking.return_date = return_date[i]
                booking.save()

            messages.success(request, "Saving Booking.")
            return redirect(reverse('booking-edit') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)
        else:
            return redirect('booking-edit')
