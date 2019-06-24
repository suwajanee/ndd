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

            template_name = 'pdf_template/agent_transport_template.html'

            if template == 'forward':
                context['trip'] = [1]
                context['work_type'] = '/1'
            elif template == 'backward':
                context['trip'] = [2]
                context['work_type'] = '/2'
            elif template == 'yard_ndd':
                context['trip'] = [1]
                context['ndd'] = [2]
                context['work_type'] = '.1'
            elif template == 'ndd_return':
                context['trip'] = [2]
                context['ndd'] = [1]
                context['work_type'] = '.2'
            else:
                context['trip'] = [1, 2]

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
            