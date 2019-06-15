# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..models import AgentTransport
from booking.views.print_view import render_pdf
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

        return render_pdf(template_name, context)
    
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
            elif template == 'yard_ndd':
                template_name = 'pdf_template/agent_transport_yard_ndd_template.html'
            elif template == 'ndd_return':
                template_name = 'pdf_template/agent_transport_ndd_return_template.html'
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

        return render_pdf(template_name, context)
            