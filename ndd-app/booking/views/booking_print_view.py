# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.db.models import Q
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

    def get(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['booking'] = get_object_or_404(Booking, pk=pk)

        if request.session['template_name']:               
            template_name = request.session['template_name']
            address = request.session['address']

            if address == 'other':
                context['address'] = request.session['address_other']
                request.session['address_other'] = context['address']
            elif address == 'shipper':
                try:
                    shipper = Shipper.objects.get(Q(principal=context['booking'].principal) & Q(name=context['booking'].shipper))
                    context['address'] = shipper.address
                except Shipper.DoesNotExist:
                    context['address'] = ''
            else:
                context['address'] = ''

            request.session['template_name'] = template_name
            request.session['address'] = address

        return self.render(template_name, context)
    
    def post(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['booking'] = get_object_or_404(Booking, pk=pk)

        if request.method == "POST":
            template = request.POST["template"]
            address = request.POST["address"+pk]
            
            if template == 'forward':
                template_name = 'pdf_template/booking_fw_template.html'
            elif template == 'backward':
                template_name = 'pdf_template/booking_bw_template.html'
            elif template == 'yard_ndd':
                template_name = 'pdf_template/booking_yard_ndd_template.html'
            elif template == 'ndd_fac_return':
                template_name = 'pdf_template/booking_ndd_fac_return_template.html'
            elif template == 'ndd_fac_ndd':
                template_name = 'pdf_template/booking_ndd_fac_ndd_template.html'
            elif template == 'ndd_return':
                template_name = 'pdf_template/booking_ndd_return_template.html'
            else:
                template_name = 'pdf_template/booking_full_template.html'
            
            if address == 'other':
                context['address'] = request.POST["address_other"]
                request.session['address_other'] = context['address']
            elif address == 'shipper':
                try:
                    shipper = Shipper.objects.get(Q(principal=context['booking'].principal) & Q(name=context['booking'].shipper))
                    context['address'] = shipper.address
                except Shipper.DoesNotExist:
                    context['address'] = ''
            else:
                context['address'] = ''

        request.session['template_name'] = template_name
        request.session['address'] = address

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
            