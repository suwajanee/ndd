# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from ..models import Booking


class BookingTableView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def render_table_booking_page(request):
        template_name = 'booking/booking_table.html'

        context = {}
        context['tmr'] = datetime.now() + timedelta(days=1)
        context['today'] = datetime.now()
        context['nbar'] = 'booking-table'

        if request.method == "GET":
            context['filter_by'] = request.GET.get("filter_by")
            context['date_filter'] = request.GET.get("date_filter")
            
            if context['date_filter'] == None:
                context['date_filter'] = ''

            if not context['date_filter']:
                context['bookings'] = Booking.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | Q(return_tr='')).order_by('date', 'work_id')
            else:
                if context['filter_by'] == "month":
                    month_of_year = datetime.strptime(context['date_filter'], '%Y-%m')
                    context['bookings'] = Booking.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | ((Q(closing_date__lte=context['tmr']) | Q(date__lte=context['today'])) & (Q(return_tr='') & Q(cancel=0)))).order_by('date', 'work_id')
                else:
                    context['bookings'] = Booking.objects.filter(Q(date=context['date_filter']) | ((Q(closing_date__lte=context['tmr']) | Q(date__lte=context['today'])) & (Q(return_tr='') & Q(cancel=0)))).order_by('date', 'work_id')

        else:
            context['bookings'] = Booking.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | Q(return_tr='')).order_by('date', 'work_id')

        return render(request, template_name, context)

