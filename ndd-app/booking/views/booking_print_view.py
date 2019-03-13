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
from .print_view import render_pdf
from customer.models import ShipperAddress
from ndd.settings import STATICFILES_DIRS


class BookingPrintView(TemplateView):

    def get(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['booking'] = get_object_or_404(Booking, pk=pk)

        if request.session['template_name'+pk]:               
            template_name = request.session['template_name'+pk]
            context['address'] = request.session['address'+pk]

            request.session['template_name'+pk] = template_name
            request.session['address'+pk] = context['address']

        return render_pdf(template_name, context)
    
    def post(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['booking'] = get_object_or_404(Booking, pk=pk)

        if request.method == "POST":
            template = request.POST["template"]
            address = request.POST["address"]
            
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
            elif address == 'none':
                context['address'] = ''
            else:
                try:
                    shipper_address = ShipperAddress.objects.get(pk=address)
                    context['address'] = shipper_address.address
                except ShipperAddress.DoesNotExist:
                    context['address'] = ''

        request.session['template_name'+pk] = template_name
        request.session['address'+pk] = context['address'] 

        return render_pdf(template_name, context)
            