# -*- coding: utf-8 -*-

from django.http import HttpResponse

import re
import xlwt

from ..models import Invoice, InvoiceDetail
from .utils_report import StyleXls
from agent_transport.models import AgentTransport
from customer.models import Shipper


def report_export(request):
    if request.method == 'POST':
        report_name = request.POST['report_name']
        invoice_id = request.POST['invoice_id']
        title = request.POST['title']

        style_xls = StyleXls()

        report_name = re.sub('[^a-zA-Z0-9 ]+', '-', report_name)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="REPORT ' + title + ' (' + report_name + ').xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        sheet = wb.add_sheet(report_name)

        # Col width
        sheet.col(0).width = 250*7
        sheet.col(1).width = 250*21
        sheet.col(2).width = 250*21
        sheet.col(3).width = 250*15
        sheet.col(4).width = 250*15
        sheet.col(5).width = 250*11
        sheet.col(6).width = 250*19
        sheet.col(7).width = 250*19
        sheet.col(8).width = 250*9
        sheet.col(9).width = 250*20
        sheet.col(10).width = 250*14
        sheet.col(11).width = 250*14

        # Sheet header
        title_style = style_xls.title_style()
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 20*22
        sheet.write_merge(0, 0, 0, 11, title, title_style)

        style = xlwt.XFStyle()
        style.font = style_xls.font_size_13()
        style.alignment = style_xls.align_left()
        sheet.write(1, 0, 'INV. NO.', style)

        style = xlwt.XFStyle()
        style.pattern = style_xls.bg_turquoise()
        sheet.row(1).height_mismatch = True
        sheet.row(1).height = 20*22
        sheet.write(1, 1, '', style)

        header_style = style_xls.header_style()

        columns = ['Item', 'Customer Name', 'BOOKING', 'From', 'To', 'Date', 'Container No. 1', 'Container No.2', 'Size', 'Drayage Charge', 'Gate Charge', 'Remark']

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

        # Detail
        invoice = Invoice.objects.get(pk=invoice_id)
        invoice_details = InvoiceDetail.objects.filter(invoice=invoice).values_list('drayage_charge', 'gate_charge', 'detail').order_by('work_agent_transport__date', 'pk')
        
        work_id = InvoiceDetail.objects.filter(invoice=invoice).values_list('work_agent_transport').order_by('work_agent_transport__date', 'pk')
        works = AgentTransport.objects.filter(pk__in=work_id).values_list('booking_no', 'pickup_from', 'return_to', 'date', 'container_1', 'container_2', 'size', 'shipper').order_by('date', 'pk')

        style = xlwt.XFStyle()
        style.font = style_xls.font_size_13()
        style.alignment = style_xls.align_left()
        if 'other' in invoice.detail:
            sheet.write_merge(1, 1, 10, 11, invoice.detail['other'], style)

        if 'customer_name' in invoice.detail:
            customer_name = invoice.detail['customer_name']
        else:
            customer_name = ''
        
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

            work = works[index]

            style.alignment = style_xls.align_left()
            if customer_name:
                sheet.write(row_num, 1, customer_name, style)
            else:
                shipper_name = Shipper.objects.get(pk=work[7])
                sheet.write(row_num, 1, shipper_name.name, style)

            style.alignment = style_xls.align_center()
            size = work[6]
            for col_num in range(len(works[index])-1):
                if col_num == 3:
                    style.num_format_str = 'D MMM YY'
                    sheet.write(row_num, col_num+2, work[col_num], style)

                elif col_num == 5:
                    if '2X' in size:
                        sheet.write(row_num, col_num+2, work[5], style)
                    else:
                        sheet.write(row_num, col_num+2, '', style)

                elif col_num == 6:
                    if not 'X' in size:
                        size = '1X' + size
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

            sheet.write(row_num, 9, drayage, style)

            if row[1]['gate']:
                gate = float(eval(row[1]['gate']))
            else:
                gate = 0
            sheet.write(row_num, 10, gate, style)

            style.alignment = style_xls.align_center()
            style.font = style_xls.font_size_13()
            style.num_format_str = 'general'
            if 'remark' in row[2]:
                sheet.write(row_num, 11, row[2]['remark'], style)
            else:
                sheet.write(row_num, 11, '', style)

            index += 1
            row_num += 1

        sheet.row(row_num).height_mismatch = True
        sheet.row(row_num + 1).height_mismatch = True
        sheet.row(row_num).height = 20*25
        sheet.row(row_num + 1).height = 20*25

        style.font = style_xls.font_size_18_bold()
        style.pattern = style_xls.bg_tan()

        sheet.write_merge(row_num, row_num, 0, 8, 'Total', style)
        sheet.write_merge(row_num + 1, row_num + 1, 0, 8, ' G.Total', style)

        sheet.write(row_num, 11, '', style)
        sheet.write(row_num + 1, 11, '', style)

        style.font = style_xls.font_size_16_bold()
        style.alignment = style_xls.align_right()
        style.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        sheet.write_merge(row_num + 1, row_num + 1, 9, 10, xlwt.Formula("J" + str(row_num+1) + "+K" + str(row_num+1)), style)

        style.font = style_xls.font_size_14_bold()
        sheet.write(row_num, 9, xlwt.Formula("SUM(J5:J" + str(row_num) + ")"), style)
        sheet.write(row_num, 10, xlwt.Formula("SUM(K5:K" + str(row_num) + ")"), style)

        wb.save(response)
        return response
    return False
