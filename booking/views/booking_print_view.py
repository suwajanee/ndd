# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

from ..models import Booking
from customer.models import Shipper

import xhtml2pdf.pisa as pisa
from django.utils.six import BytesIO
import os

# from weasyprint import HTML, CSS

class BookingPrintView(TemplateView):
    
    def get(self, request, pk, template):
        if template == 'forward':
            template_name = 'pdf_template/fw_template.html'
        elif template == 'backward':
            template_name = 'pdf_template/bw_template.html'
        else:
            template_name = 'pdf_template/full_template.html'

        booking = get_object_or_404(Booking, pk=pk)
        base_dir = os.path.dirname(os.path.dirname(__file__))

        if booking.address == 'other':
            address = booking.address_other
        elif booking.address == 'shipper':
            shipper = Shipper.objects.get(name=booking.shipper)
            address = shipper.address
        else:
            address = ''

        return self.render(template_name, {'booking': booking, 'address': address,'base_dir': base_dir})

    def render(self, path, params):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
            