# -*- coding: utf-8 -*-

import xlwt
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from booking.models import Booking
from .utils_oocl import StyleXls
from agent_transport.models import AgentTransport
from customer.models import Principal, Shipper
from ..models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from ..serializers import SummaryWeekSerializer, SummaryCustomerSerializer, InvoiceSerializer, CustomerCustomSerializer, InvoiceDetailSerializer


def oocl_report(request):
    if request.method == 'POST':
        report_name = request.POST['report_name']
        invoice_id = request.POST['invoice_id']

        style_xls = StyleXls()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="REPORT OOCL (' + report_name + ').xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        sheet = wb.add_sheet(report_name)

        # sheet.paper_size_code = 9
        # sheet.show_auto_page_breaks = 1
        # sheet.fit_num_pages=1

        # Col width
        sheet.col(0).width = 250*7
        sheet.col(1).width = 250*21
        sheet.col(2).width = 250*21
        sheet.col(3).width = 250*15
        sheet.col(4).width = 250*15
        sheet.col(5).width = 250*11
        sheet.col(6).width = 250*19
        sheet.col(7).width = 250*9
        sheet.col(8).width = 250*20
        sheet.col(9).width = 250*14
        sheet.col(10).width = 250*14

        # Sheet header
        title_style = style_xls.title_style()
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 20*22
        sheet.write_merge(0, 0, 0, 10, 'OOCL', title_style)

        style = xlwt.XFStyle()
        style.font = style_xls.font_size_13()
        style.alignment = style_xls.align_left()
        sheet.write(1, 0, 'INV. NO.', style)

        style = xlwt.XFStyle()
        style.pattern = style_xls.bg_turquoise()
        sheet.row(1).height_mismatch = True
        sheet.row(1).height = 20*22
        sheet.write(1, 1, ' ', style)

        header_style = style_xls.header_style()

        columns = ['Item', 'Customer Name', 'BOOKING', 'From', 'To', 'Date', 'Container No. 1', 'Size', 'Drayage Charge', 'Gate Charge', 'Remark']

        sheet.row(2).height_mismatch = True
        sheet.row(3).height_mismatch = True

        sheet.row(2).height = 20*20
        sheet.row(3).height = 20*20

        sheet.write_merge(2, 2, 3, 4, 'Vessel/Truck Routing', header_style)

        for col_num in range(len(columns)):
            if col_num < 3 or col_num > 4 :
                sheet.write_merge(2, 3, col_num, col_num, columns[col_num], header_style)
            else:
                sheet.write(3, col_num, columns[col_num], header_style)

        invoice = Invoice.objects.get(pk=invoice_id)
        invoice_details = InvoiceDetail.objects.filter(invoice=invoice).values_list('drayage_charge', 'gate_charge', 'detail').order_by('work_agent_transport__date', 'pk')
        
        work_id = InvoiceDetail.objects.filter(invoice=invoice).values_list('work_agent_transport').order_by('work_agent_transport__date', 'pk')
        works = AgentTransport.objects.filter(pk__in=work_id).values_list('booking_no', 'pickup_from', 'return_to', 'date', 'container_1', 'size')

        if 'customer_name' in invoice.detail:
            customer_name = invoice.detail['customer_name']
        else:
            customer_name = 'OOCL'
        
        row_num = 4
        index = 0

        style = xlwt.XFStyle()
        style.borders = style_xls.border_cell()
        style.alignment = style_xls.align_center()
        style.font = style_xls.font_size_13()

        for row in invoice_details:
            sheet.row(row_num).height_mismatch = True
            sheet.row(row_num).height = 20*20

            col_num = 0
            
            sheet.write(row_num, 0, index+1, style)

            style.alignment = style_xls.align_left()
            sheet.write(row_num, 1, customer_name, style)

            style.alignment = style_xls.align_center()

            work = works[index]
            for col_num in range(len(works[index])):
                if col_num == 3:
                    style.num_format_str = 'D MMM YY'
                    sheet.write(row_num, col_num+2, work[col_num], style)

                elif col_num == 5:
                    size = work[col_num]
                    if not 'X' in size:
                        size = '1X' + work[col_num]
                    sheet.write(row_num, col_num+2, size, style)   
                else:
                    sheet.write(row_num, col_num+2, work[col_num], style)

                style.num_format_str = 'general'

            style.alignment = style_xls.align_right()
            style.font = style_xls.font_size_14()
            style.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'

            if row[0]['drayage']:
                drayage = float(eval(row[0]['drayage']))
            else:
                drayage = 0

            sheet.write(row_num, 8, drayage, style)

            if row[1]['gate']:
                gate = float(eval(row[1]['gate']))
            else:
                gate = 0
            sheet.write(row_num, 9, gate, style)

            style.alignment = style_xls.align_center()
            style.font = style_xls.font_size_13()
            style.num_format_str = 'general'
            if 'remark' in row[2]:
                sheet.write(row_num, 10, row[2]['remark'], style)
            else:
                sheet.write(row_num, 10, '', style)

            index += 1
            row_num += 1

        sheet.row(row_num).height_mismatch = True
        sheet.row(row_num + 1).height_mismatch = True
        sheet.row(row_num).height = 20*25
        sheet.row(row_num + 1).height = 20*25

        style.font = style_xls.font_size_18_bold()
        style.pattern = style_xls.bg_tan()

        sheet.write_merge(row_num, row_num, 0, 7, 'Total', style)
        sheet.write_merge(row_num + 1, row_num + 1, 0, 7, ' G.Total', style)

        sheet.write(row_num, 10, '', style)
        sheet.write(row_num + 1, 10, '', style)

        style.font = style_xls.font_size_16_bold()
        style.alignment = style_xls.align_right()
        style.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        sheet.write_merge(row_num + 1, row_num + 1, 8, 9, xlwt.Formula("I" + str(row_num+1) + "+J" + str(row_num+1)), style)


        style.font = style_xls.font_size_14_bold()
        # sheet.write(row_num, 8, invoice.drayage_total, style)
        sheet.write(row_num, 8, xlwt.Formula("SUM(I5:I" + str(row_num) + ")"), style)
        # if invoice.gate_total:
        sheet.write(row_num, 9, xlwt.Formula("SUM(J5:J" + str(row_num) + ")"), style)
        # else:
        #     sheet.write(row_num, 9, 0, style)

        wb.save(response)
        return response
    return False
