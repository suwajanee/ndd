# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.utils.six import BytesIO
from django.views.generic import TemplateView

import xhtml2pdf.pisa as pisa

from ..models import Booking
from customer.models import Shipper
from ndd.settings import STATICFILES_DIRS


class BookingPrintView(TemplateView):
    
    def get(self, request, pk, template):
        if template == 'forward':
            template_name = 'pdf_template/booking_fw_template.html'
        elif template == 'backward':
            template_name = 'pdf_template/booking_bw_template.html'
        else:
            template_name = 'pdf_template/booking_full_template.html'
            
        context = {}
        context['booking'] = get_object_or_404(Booking, pk=pk)
        context['static_dir'] = STATICFILES_DIRS[0]

        if context['booking'].address == 'other':
            context['address'] = booking.address_other
        elif context['booking'].address == 'shipper':
            try:
                shipper = Shipper.objects.get(name=context['booking'].shipper)
                context['address'] = shipper.address
            except Shipper.DoesNotExist:
                context['address'] = ''
        else:
            context['address'] = ''

        return self.render(template_name, context)

    def print_time(request):
        booking_print_view = BookingPrintView()
        template_name = 'pdf_template/booking_time_template.html'
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        if request.method == "POST":
            pk_list = request.POST.getlist("pk")
            context['bookings'] = Booking.objects.filter(pk__in=pk_list).order_by('date', 'work_id')
            request.session['pk_list'] = pk_list
        else:
            if request.session['pk_list']:
                pk_list = request.session['pk_list']
                context['bookings'] = Booking.objects.filter(pk__in=pk_list).order_by('date', 'work_id')

                request.session['pk_list'] = pk_list
        
        return booking_print_view.render(template_name, context)

    def render(self, path, params):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
            