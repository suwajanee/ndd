# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.utils.six import BytesIO
from django.views.generic import TemplateView

import xhtml2pdf.pisa as pisa

from ..models import AgentTransport
from customer.models import ShipperAddress
from ndd.settings import STATICFILES_DIRS


class AgentTransportPrintView(TemplateView):

    def get(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['agent_transport'] = get_object_or_404(AgentTransport, pk=pk)

        if request.session['template_name'+pk]:               
            template_name = request.session['template_name'+pk]
            context['address'] = request.session['address'+pk]

            request.session['template_name'+pk] = template_name
            request.session['address'+pk] = context['address']

        return self.render(template_name, context)
    
    def post(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['agent_transport'] = get_object_or_404(AgentTransport, pk=pk)

        if request.method == "POST":
            template = request.POST["template"]
            address = request.POST["address"]

            if template == 'forward':
                template_name = 'pdf_template/agent_transport_fw_template.html'
            elif template == 'backward':
                template_name = 'pdf_template/agent_transport_bw_template.html'
            else:
                template_name = 'pdf_template/agent_transport_full_template.html'

            if address == 'other':
                context['address'] = request.POST["address_other"]
            elif address == 'none':
                context['address'] = ''
            else:
                try:
                    shipper_address = ShipperAddress.objects.get(pk=address)
                    context['address'] = shipper_address.address
                except Shipper.DoesNotExist:
                    context['address'] = ''

        request.session['template_name'+pk] = template_name
        request.session['address'+pk] = context['address']

        return self.render(template_name, context)
        
    def render(self, path, params):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response, encoding="UTF-8")
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)
            