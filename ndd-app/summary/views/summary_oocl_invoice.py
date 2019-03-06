# -*- coding: utf-8 -*-

import xlwt
import copy
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ndd.settings import STATICFILES_DIRS
from booking.models import Booking
from .utils_oocl import StyleXls
from agent_transport.models import AgentTransport
from customer.models import Principal, Shipper
from ..models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from ..serializers import SummaryWeekSerializer, SummaryCustomerSerializer, InvoiceSerializer, CustomerCustomSerializer, InvoiceDetailSerializer


def oocl_invoice(request):
    if request.method == 'POST':
        # report_name = request.POST['report_name']
        invoice_id = request.POST['invoice_id']

        invoice = Invoice.objects.get(pk=invoice_id)

        week = "{:0>2s}".format(invoice.customer_week.week.week)

        style_xls = StyleXls()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="WK.' + week + ' ' + invoice.invoice_no + '.xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        sheet = wb.add_sheet(invoice.invoice_no)

        sheet.header_str = bytes('', 'utf-8')
        sheet.footer_str = bytes('', 'utf-8')

        # Col width
        sheet.col(0).width = 256*1
        sheet.col(1).width = 256*6
        sheet.col(2).width = 256*28
        sheet.col(3).width = 256*10
        sheet.col(4).width = 256*14
        sheet.col(5).width = 256*20
        sheet.col(6).width = 256*18

        # Sheet header
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 20*27

        for row in range(1, 6):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 20*21
        for row in range(7, 13):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 10*39
        sheet.row(13).height_mismatch = True
        sheet.row(13).height = 465
        for row in range(14, 25):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 10*45
        for row in range(25, 29):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 465
        for row in range(29, 34):
            if row == 32:
                continue
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 20*21
        sheet.row(32).height_mismatch = True
        sheet.row(32).height = 555
        
        
        image = STATICFILES_DIRS[0] + '/images/logo.bmp'
        sheet.insert_bitmap(image, 0, 1, 25, 5)

        style = xlwt.XFStyle()
        style.alignment = style_xls.align_left()
        style.font = style_xls.font_size_18_bold()
        sheet.write(0, 3, 'N&DD INTERNATIONAL (THAILAND) CO.,LTD.', style)

        style.font = style_xls.font_size_14()
        sheet.write(1, 3, '10/19 Moo.4 Bangchalong Subdistrict, Bangplee District,', style)
        sheet.write(2, 3, 'Samutprakarn 10540 Tel : 02-1305977-78 Fax : 02-1305979', style)
        sheet.write(3, 3, 'TAX ID : 0105540102061 / Head Office', style)


        sheet.row(6).height_mismatch = True
        sheet.row(6).height = 20*34

        style.alignment = style_xls.align_center()
        style.font = style_xls.font_size_18_bold()
        style.borders = style_xls.border_cell()
        sheet.write_merge(6, 6, 1, 6, 'INVOICE', style)


        style = xlwt.XFStyle()
        style.alignment = style_xls.align_left()
        style.borders = style_xls.border_left()
        style.font = style_xls.font_size_16_bold()
        sheet.write(7, 1, 'Customer Name : ', style)

        style.font = style_xls.font_size_14()
        sheet.write(8, 1, 'ORIENT OVERSEAS CONTAINER LINE LTD.', style)
        sheet.write(9, 1, 'OOCL (THAILAND) LTD. AS AN AGENT', style)
        sheet.write(10, 1, '76/68-69 OCEAN TOWER II,29 th., SOI SUKHUMVIT 19,', style)
        sheet.write(11, 1, 'KLONGTOEY NUA, WATTANA BANGKOK 10110', style)
        sheet.write(12, 1, 'TAX ID : 0993000037774 / Head Office', style)


        style = xlwt.XFStyle()
        style.alignment = style_xls.align_left()
        style.font = style_xls.font_size_14_bold()
        sheet.write(7, 5, 'INVOICE NO.', style)
        sheet.write(8, 5, 'DATE :', style)
        sheet.write(9, 5, 'AP BILLING NO.', style)

        style.font = style_xls.font_size_16()
        style.borders = style_xls.border_right()
        sheet.write(7, 6, invoice.invoice_no, style)
        sheet.write(9, 6, invoice.detail['other'], style)
        sheet.write(10, 6, '', style)
        sheet.write(11, 6, '', style)
        sheet.write(12, 6, '', style)

        style.num_format_str = 'D MMM YYYY'
        sheet.write(8, 6, invoice.customer_week.date_billing, style)

        invoice_details = InvoiceDetail.objects.filter(invoice=invoice)
        size_20_1 = invoice_details.filter(work_agent_transport__size__startswith='20')
        size_20_2 = invoice_details.filter(work_agent_transport__size__contains='2X20')

        count_20_1 = size_20_1.count()
        count_20_2 = size_20_2.count()*2
        count_20 = count_20_1 + count_20_2
        if count_20_2 > 0:
            price_20 = eval(size_20_2[0].drayage_charge['drayage'])/2
        elif count_20_1 > 1:
            price_20 = eval(size_20_1[0].drayage_charge['drayage'])
        else:
            price_20 = 0

        size_40 = invoice_details.filter(work_agent_transport__size__contains='40')
        count_40 = size_40.count()
        if count_40 > 0:
            price_40 = eval(size_40[0].drayage_charge['drayage'])
        else:
            price_40 = 0


        style = style_xls.header_style()
        style.font = style_xls.font_size_16_bold()
        sheet.write(13, 1, 'No.', style)
        sheet.write_merge(13, 13, 2, 3, 'Description', style)
        sheet.write(13, 4, 'Unit', style)
        sheet.write(13, 5, 'Unit Price', style)
        sheet.write(13, 6, 'Amount', style)

        style = xlwt.XFStyle()
        style.font = style_xls.font_size_16()
        style.borders = style_xls.border_left_right()

        style_c = copy.deepcopy(style)
        style_l = copy.deepcopy(style)
        style_r = copy.deepcopy(style)

        style_c.alignment = style_xls.align_center()
        style_l.alignment = style_xls.align_left()
        style_r.alignment = style_xls.align_right()

        style_r.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'

        sheet.write(14, 1, '1', style_c)

        if count_20 > 0:
            sheet.write_merge(14, 14, 2, 3, "Container Transportation Charge 20'", style_l)
            sheet.write(14, 4, count_20, style_c)
            sheet.write(14, 5, price_20, style_r)
        elif count_40 > 0:
            sheet.write_merge(14, 14, 2, 3, "Container Transportation Charge 40'", style_l)
            sheet.write(14, 4, count_40, style_c)
            sheet.write(14, 5, price_40, style_r)
        sheet.write(14, 6, xlwt.Formula("E15*F15"), style_r)

        if count_20 > 0 and count_40 > 0:
            sheet.write(15, 1, '2', style_c)
            sheet.write_merge(15, 15, 2, 3, "Container Transportation Charge 40'", style_l)
            sheet.write(15, 4, count_40, style_c)
            sheet.write(15, 5, price_40, style_r)
            sheet.write(15, 6, xlwt.Formula("E16*F16"), style_r)
        else:
            sheet.write(15, 1, '', style_c)
            sheet.write_merge(15, 15, 2, 3, '', style_l)
            sheet.write(15, 4, '', style_c)
            sheet.write(15, 5, '', style_r)
            sheet.write(15, 6, '', style_r)

        for row in range(16, 25):
            if row == 24:
                style.borders = style_xls.border_left_right_bottom()
            sheet.write(row, 1, '', style)
            sheet.write_merge(row, row, 2, 3, '', style)
            sheet.write(row, 4, '', style)
            sheet.write(row, 5, '', style)
            sheet.write(row, 6, '', style)

        style.borders = style_xls.border_left()
        style.font = style_xls.font_size_16_bold()
        style.alignment = style_xls.align_left()
            
        sheet.write_merge(25, 25, 1, 4, 'Remark :', style)
        sheet.write_merge(26, 26, 1, 4, '', style)
        sheet.write_merge(27, 27, 1, 4, '', style)

        style.borders = style_xls.border_left_bottom()
        style.font = style_xls.font_size_12()
        style.alignment = style_xls.align_center()
        sheet.write_merge(28, 28, 1, 4, '', style)

        style.borders = style_xls.border_right()
        style.font = style_xls.font_size_16_bold()
        style.alignment = style_xls.align_left()
        sheet.write(25, 5, 'Sub Total', style)
        sheet.write(26, 5, 'Gross Total', style)
        sheet.write(27, 5, 'Withholding Tax 1%', style)

        style.borders = style_xls.border_right_bottom()
        sheet.write(28, 5, 'Grand Total', style)

        style.borders = style_xls.border_right()
        style.font = style_xls.font_size_16()
        style.alignment = style_xls.align_right()
        style.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        sheet.write(25, 6, xlwt.Formula("SUM(G15:G25)"), style)
        sheet.write(26, 6, xlwt.Formula("SUM(G26)"), style)
        sheet.write(27, 6, xlwt.Formula("G27*1%"), style)

        style.borders = style_xls.border_right_bottom()
        sheet.write(28, 6, xlwt.Formula("SUM(G27-G28)"), style)


        style = xlwt.XFStyle()
        style.borders = style_xls.border_left()
        style.alignment = style_xls.align_left()
        sheet.write_merge(29, 29, 1, 4, '', style)
        sheet.write_merge(30, 30, 1, 4, '', style)

        style.font = style_xls.font_size_14_bold()
        sheet.write_merge(31, 31, 1, 4, 'Recipient Billing :', style)

        style.font = style_xls.font_size_14()
        sheet.write_merge(32, 32, 1, 4, '_________________ Date ____/_____/______', style)

        style.borders = style_xls.border_left_bottom()
        sheet.write_merge(33, 33, 1, 4, '', style)

        style.borders = style_xls.border_right()
        sheet.write_merge(29, 29, 5, 6, 'Please make payment by crossed cheque', style)
        sheet.write_merge(30, 30, 5, 6, 'and payable to :', style)

        style.font = style_xls.font_size_12()
        style.alignment = style_xls.align_center()
        sheet.write_merge(31, 31, 5, 6, 'N&DD INTERNATIONAL (THAILAND) CO.,LTD.', style)

        style.font = style_xls.font_size_14_bold()
        style.alignment = style_xls.align_left()
        sheet.write_merge(32, 32, 5, 6, 'Authorized Signatre ______________________', style)

        style.borders = style_xls.border_right_bottom()
        style.font = style_xls.font_size_14()
        style.alignment = style_xls.align_right()
        sheet.write_merge(33, 33, 5, 6, 'Date ____/_____/______  ', style)

        wb.save(response)
        return response
    return False
