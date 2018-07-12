# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
from django.template.loader import get_template

from ..models import Booking

import xhtml2pdf.pisa as pisa
from django.utils.six import BytesIO
import os


class BookingPrintView(TemplateView):
    
    template_name = 'order_template.html'
        
    def get(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        base_dir = os.path.dirname(os.path.dirname(__file__)) 
        return self.render(self.template_name, {'booking': booking, 'base_dir': base_dir})

    def render(self, path, params):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
            