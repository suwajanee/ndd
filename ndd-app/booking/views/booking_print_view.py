# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..models import Booking
from .print_view import render_pdf
from customer.models import ShipperAddress
from ndd.settings import STATICFILES_DIRS


class BookingPrintView(TemplateView):

    def post(self, request, pk):
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        context['booking'] = get_object_or_404(Booking, pk=pk)

        if request.method == "POST":
            template = request.POST["template"]
            address = request.POST["address"]

            template_name = 'pdf_template/booking_template.html'
            
            if template == 'yard_ndd':
                context['trip'] = [1]
                context['ndd'] = [2]
                context['work_type'] = '/1.1'
            elif template == 'yard_fac_ndd':
                context['trip'] = [1, 2]
                context['ndd'] = [4]
                context['work_type'] = '/1.2'            
            elif template == 'ndd_fac_ndd':
                context['trip'] = [1, 2]
                context['ndd'] = [1, 4]
                context['work_type'] = '/2.1'
            elif template == 'ndd_fac_return':
                context['trip'] = [1, 2]
                context['ndd'] = [1]
                context['work_type'] = '/2.2'
            elif template == 'ndd_return':
                context['trip'] = [2]
                context['ndd'] = [3]
                context['work_type'] = '/3.1'
            elif template == 'forward':
                context['trip'] = [1]
                context['work_type'] = '/4.1'
            elif template == 'ndd_fac':
                context['trip'] = [1]
                context['ndd'] = [1]
                context['work_type'] = '/4.2'
            elif template == 'backward':
                context['trip'] = [2]
                context['work_type'] = '/5.1'
            elif template == 'fac_ndd':
                context['trip'] = [2]
                context['ndd'] = [4]
                context['work_type'] = '/5.2'
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
                except ShipperAddress.DoesNotExist:
                    context['address'] = ''
            if "couple" in request.POST:
                context['couple'] = True
                booking_2 = Booking.objects.filter(work_id=request.POST["work_with"].strip())
                if len(booking_2):
                    context['booking_2'] = booking_2[0]
                
                if 'couple_address' in request.POST:
                    address_2 = request.POST["address_2"]
                    context['couple_address'] = True
                    if address_2 == 'other':
                        context['address_2'] = request.POST["address_other_2"]
                    elif address_2 == 'none':
                        context['address_2'] = ''
                    else:
                        try:
                            shipper_address_2 = ShipperAddress.objects.get(pk=address_2)
                            context['address_2'] = shipper_address_2.address
                        except ShipperAddress.DoesNotExist:
                            context['address_2'] = ''

        return render_pdf(template_name, context)
            