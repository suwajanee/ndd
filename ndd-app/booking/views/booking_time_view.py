# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import Booking


class BookingTimeView(TemplateView):
    
    @login_required(login_url=reverse_lazy('login'))
    def render_time_booking_page(request):
        template_name = 'booking/booking_time.html'
        context = {}
        context['nbar'] = 'booking-table'
        context['tmr'] = datetime.now() + timedelta(days=1)
        context['today'] = datetime.now()

        if request.method == "POST":
            pk_list = request.POST.getlist("pk")
            context['filter_by'] = request.POST['filter_by']
            context['date_filter'] = request.POST['date_filter']

            context['bookings'] = Booking.objects.filter(pk__in = pk_list).order_by('date', 'work_id')

            request.session['pk_list'] = pk_list
            request.session['filter_by'] = context['filter_by']
            request.session['date_filter'] = context['date_filter']

            return render(request, template_name, context)
        else:
            if request.session['pk_list']:
                pk_list = request.session['pk_list']
                context['filter_by'] = request.session['filter_by']
                context['date_filter'] = request.session['date_filter']
                context['bookings'] = Booking.objects.filter(pk__in=pk_list).order_by('date', 'work_id')

                request.session['pk_list'] = pk_list
                request.session['date_filter'] = context['date_filter']
                request.session['filter_by'] = context['filter_by']

                return render(request, template_name, context)
            else:
                filter_by = request.GET.get("filter_by")
                date_filter = request.GET.get("date_filter")
                if not date_filter:
                    return redirect('booking-table')
                else:
                    return redirect('booking-table' + '?filter_by=' + filter_by + '&date_filter=' + date_filter)

    @login_required(login_url=reverse_lazy('login'))
    def save_time_booking(request):
        if request.method == 'POST':
            pk = request.POST.getlist('pk')
            pickup_in_time_1 = request.POST.getlist('pickup_in_time_1')
            pickup_in_time_2 = request.POST.getlist('pickup_in_time_2')

            pickup_out_time_1 = request.POST.getlist('pickup_out_time_1')
            pickup_out_time_2 = request.POST.getlist('pickup_out_time_2')

            factory_in_time_1 = request.POST.getlist('factory_in_time_1')
            factory_in_time_2 = request.POST.getlist('factory_in_time_2')

            factory_load_start_time_1 = request.POST.getlist('factory_load_start_time_1')
            factory_load_start_time_2 = request.POST.getlist('factory_load_start_time_2')

            factory_load_finish_time_1 = request.POST.getlist('factory_load_finish_time_1')
            factory_load_finish_time_2 = request.POST.getlist('factory_load_finish_time_2')

            factory_out_time_1 = request.POST.getlist('factory_out_time_1')
            factory_out_time_2 = request.POST.getlist('factory_out_time_2')

            return_in_time_1 = request.POST.getlist('return_in_time_1')
            return_in_time_2 = request.POST.getlist('return_in_time_2')

            return_out_time_1 = request.POST.getlist('return_out_time_1')
            return_out_time_2 = request.POST.getlist('return_out_time_2')
            
            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            for i in range(0,len(pk)):
                booking = Booking.objects.get(pk=pk[i])
                booking.pickup_in_time = pickup_in_time_1[i] + '//' + pickup_in_time_2[i]
                booking.pickup_out_time = pickup_out_time_1[i] + '//' + pickup_out_time_2[i]
                booking.factory_in_time = factory_in_time_1[i] + '//' + factory_in_time_2[i]
                booking.factory_load_start_time = factory_load_start_time_1[i] + '//' + factory_load_start_time_2[i]
                booking.factory_load_finish_time = factory_load_finish_time_1[i] + '//' + factory_load_finish_time_2[i]
                booking.factory_out_time = factory_out_time_1[i] + '//' + factory_out_time_2[i]
                booking.return_in_time = return_in_time_1[i] + '//' + return_in_time_2[i]
                booking.return_out_time = return_out_time_1[i] + '//' + return_out_time_2[i]
                
                booking.save()

            messages.success(request, "Saving Booking.")
            return redirect('booking-time')
        else:
            return redirect('booking-table')