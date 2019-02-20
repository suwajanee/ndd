# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.utils.six import BytesIO
from django.views.generic import TemplateView

import xhtml2pdf.pisa as pisa

from ..models import FormDetail, Invoice, InvoiceDetail
from ..serializers import InvoiceSerializer
from customer.models import ShipperAddress
from ndd.settings import STATICFILES_DIRS
from booking.views.print_view import render_pdf


class SummaryPrintView(TemplateView):

    def get(self, request, pk):
        template_name = 'pdf_template/summary_print_template.html'
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        invoice = get_object_or_404(Invoice, pk=pk)
        context['invoice'] = invoice
        context['invoice_no'] = invoice.invoice_no.split(',')

        context['diesel_rate'] = invoice.customer_week.week.diesel_rate

        context['form'] = FormDetail.objects.all().order_by('pk').first().form_detail

        if invoice.customer_week.customer_custom:
            context['option'] = invoice.customer_week.customer_custom.option
            if invoice.customer_week.customer_custom.form:
                context['form'] = invoice.customer_week.customer_custom.form.form_detail

        invoice_details = InvoiceDetail.objects.filter(invoice=invoice).order_by('work_normal__date', 'work_agent_transport__date', 'pk')

        rows = len(invoice_details)
        num = 0

        for detail in invoice_details:
            detail.detail['num'] = num = num + 1
            if 'other' in detail.drayage_charge:
                rows += len(detail.drayage_charge['other'])
                for other in detail.drayage_charge['other']:
                    other['num'] = num = num + 1

        context['invoice_details'] = invoice_details

            

        context['rows'] = rows + 2


        return render_pdf(template_name, context)


class SummaryEvergreenPrintView(TemplateView):

    def get(self, request, pk):
        template_name = 'pdf_template/summary_evergreen_print_template.html'
        context = {}
        context['static_dir'] = STATICFILES_DIRS[0]
        invoice = get_object_or_404(Invoice, pk=pk)
        context['invoice'] = invoice

        context['diesel_rate'] = invoice.customer_week.week.diesel_rate

        context['form'] = FormDetail.objects.all().order_by('pk').first().form_detail

        if invoice.customer_week.customer_custom:
            context['option'] = invoice.customer_week.customer_custom.option
            if invoice.customer_week.customer_custom.form:
                context['form'] = invoice.customer_week.customer_custom.form.form_detail

        invoice_details = InvoiceDetail.objects.filter(invoice=invoice).order_by('work_agent_transport__date', 'pk')

        rows = len(invoice_details)
        num = 0

        for detail in invoice_details:
            detail.detail['num'] = num = num + 1
            if 'other' in detail.drayage_charge:
                rows += len(detail.drayage_charge['other'])
                for other in detail.drayage_charge['other']:
                    other['num'] = num = num + 1

        context['invoice_details'] = invoice_details

            

        context['rows'] = rows + 2


        return render_pdf(template_name, context)

