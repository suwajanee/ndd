# -*- coding: utf-8 -*-

import xlwt
import copy

from django.http import HttpResponse

from ..models import Invoice, InvoiceDetail
from .utils_damco import StyleXls


def damco_invoice(request):
    if request.method == 'POST':
        invoice_id = request.POST['invoice_id']

        invoice = Invoice.objects.get(pk=invoice_id)
        week = "{:0>2s}".format(invoice.customer_week.week.week)
        year = invoice.customer_week.week.year.year_label

        invoice_details = InvoiceDetail.objects.filter(invoice=invoice).order_by('work_normal__date', 'pk')

        style_xls = StyleXls()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Damco wk.' + week + ' (' + invoice.invoice_no + ').xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        sheet = wb.add_sheet(invoice.invoice_no)
        sheet.portrait  = 0
        sheet.fit_num_pages = 1
        sheet.preview_magn = 40
        sheet.page_preview = True

        sheet.left_margin = 0.3
        sheet.right_margin = 0.3
        sheet.top_margin = 0.3
        sheet.bottom_margin = 0.3

        sheet.header_str = bytes('', 'utf-8')
        sheet.footer_str = bytes('', 'utf-8')

        # Col width
        sheet.col(0).width = 256*16
        sheet.col(1).width = 256*23
        sheet.col(2).width = 256*19
        sheet.col(3).width = 256*34
        sheet.col(4).width = 256*29
        sheet.col(5).width = 256*45
        sheet.col(6).width = 256*54
        sheet.col(7).width = 256*30
        sheet.col(8).width = 256*18
        sheet.col(9).width = 256*13
        sheet.col(10).width = 256*34
        sheet.col(11).width = 256*23
        sheet.col(12).width = 256*26
        sheet.col(13).width = 256*30
        sheet.col(14).width = 256*20
        sheet.col(15).width = 256*19
        sheet.col(16).width = 256*22
        sheet.col(17).width = 256*25
        sheet.col(18).width = 256*19
        sheet.col(19).width = 256*34

        # Row height
        for row in range(0, 4):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 735
        for row in range(4, 8):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 20*54
        sheet.row(8).height_mismatch = True
        sheet.row(8).height = 735

        for row in range(9, 11):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 10*39
        sheet.row(11).height_mismatch = True
        sheet.row(11).height = 585

        for row in range(12, 20):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 1035

        sheet.row(20).height_mismatch = True
        sheet.row(20).height = 20*15
        for row in range(21, 31):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 20*48
        sheet.row(31).height_mismatch = True
        sheet.row(31).height = 20*18
        for row in range(32, 36):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 645
        

        # Header invoice
        style = xlwt.XFStyle()
        style.font = style_xls.font_size_30_bold()
        sheet.write_merge(4, 4, 1, 7, 'Damco Logistics (Thailand) Co., Ltd. (Head Office)', style)
        sheet.write_merge(6, 6, 1, 7, '0105534075332', style)

        style.alignment = style_xls.align_center()
        sheet.write_merge(0, 0, 0, 19, 'N&DD INTERNATIONAL (THAILAND) CO.,LTD.', style)
        sheet.write_merge(3, 3, 16, 19, 'TAX INVOICE / INVOICE (Original)', style)

        style.font = style_xls.font_size_30()
        sheet.write_merge(1, 1, 0, 19, '10/19 MOO.4 BANGCHALONG SUBDISTRICT BANGPLEE DISTRICT SAMUTPRAKARN 10540 TEL.02-1305977-78 FAX.02-1305979', style)
        sheet.write_merge(2, 2, 0, 19, 'เลขประจำตัวผู้เสียภาษี 0105540102061', style)

        style.alignment = style_xls.align_left()
        sheet.write(4, 0, 'ลูกค้า', style)
        sheet.write(5, 0, 'ที่อยู่', style)
        sheet.write(6, 0, 'No.', style)
        sheet.write_merge(5, 5, 1, 7, '1 Empire Tower, South Sathorn Road, Yannawa,  Sathorn Bangkok 10120', style)

        style.borders = style_xls.border_all()
        style.font = style_xls.font_size_28()
        style.alignment = style_xls.align_center()
        sheet.write_merge(4, 4, 16, 17, 'Invoice no.', style)
        sheet.write_merge(5, 5, 16, 17, 'Invoice Date :', style)
        sheet.write_merge(6, 6, 16, 17, 'Kewill no. / Po no.', style)
        style.font = style_xls.font_size_26()
        sheet.write_merge(4, 4, 18, 19, invoice.invoice_no, style)

        style.num_format_str = 'D-MMM-YYYY'
        sheet.write_merge(5, 5, 18, 19, invoice.customer_week.date_billing, style)

        style.num_format_str = 'general'
        style.font = style_xls.font_size_25()
        sheet.write_merge(7, 7, 16, 17, 'Customer Booking no.', style)
        sheet.write_merge(6, 6, 18, 19, '', style)
        sheet.write_merge(7, 7, 18, 19, invoice_details[0].work_normal.booking_no, style)


        # Header table
        style.font = style_xls.font_size_16_bold()
        style.alignment = style_xls.align_center_mid()
        style.pattern = style_xls.bg_light_green()

        style_head_top = copy.deepcopy(style)
        style_head_mid = copy.deepcopy(style)
        style_head_bot = copy.deepcopy(style)

        style.borders = style_xls.border_all()
        style_head_top.borders = style_xls.border_x_top()
        style_head_mid.borders = style_xls.border_x()
        style_head_bot.borders = style_xls.border_x_bottom()

        header_thai = ['ลำดับที่', 'วันที่วิ่งงาน', 'ทะเบียนรถ', 'ชื่อลูกค้า/เอเจนต์', 'เลขที่ใบจอง', 'Kewill Job number / ', 'เส้นทาง(จาก-ถึง)', 'หมายเลขตู้', 'ขนาดตู้', 'จำนวนตู้', \
                        'ค่าขนส่ง', 'ค่าขนส่งอื่นๆ', 'ค่าผ่านท่า', 'ค่ายกตู้', 'ค่าใช้จ่ายอื่น', 'ค่าแรงงาน', 'ค่าผ่านท่า', 'ค่ายกตู้', 'ค่าใช้จ่ายอื่น', 'ยอดรวม']
        header_eng = ['No.', 'Date', 'Licence no.', 'Customer/Agent name', 'Booking no.', 'Booking Job no.', 'Routing', 'Container No.', 'Size', 'Quantity', \
                        'Transport', 'Other Transprot', 'Gate', 'Lift on/off', 'Other', 'Lobour Charge', 'Gate', 'Lift on/off', 'Other', 'Total Amount']

        sheet.write_merge(9, 9, 10, 15, 'ใบเสร็จชื่อดัมโก้', style)
        sheet.write_merge(9, 9, 16, 18, 'ใบเสร็จชื่อลูกค้า', style)

        for col_num in range(len(header_thai)):
            if col_num < 10 or col_num > 18:
                sheet.write(9, col_num, header_thai[col_num], style_head_top)
                sheet.write(10, col_num, '', style_head_mid)
                sheet.write(11, col_num, header_eng[col_num], style_head_bot)
            else:
                sheet.write(10, col_num, header_thai[col_num], style_head_top)
                sheet.write(11, col_num, header_eng[col_num], style_head_bot)


        # Details
        style = xlwt.XFStyle()
        style.font = style_xls.font_size_16()
        style.borders = style_xls.border_all()
        style_currency = copy.deepcopy(style)

        style.alignment = style_xls.align_center_mid()

        style_time = copy.deepcopy(style)
        style_time.num_format_str = 'D MMM YY'

        style_currency.alignment = style_xls.align_right_mid()
        style_currency.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        
        row_num = 11
        for index, row in enumerate(invoice_details):
            work = row.work_normal
            drayage = eval(row.drayage_charge['drayage'])
            row_num += 1
            num = str(row_num + 1)
            sheet.write(row_num, 0, index+1, style)
            sheet.write(row_num, 1, work.date, style_time)
            sheet.write(row_num, 2, '', style)
            sheet.write(row_num, 3, 'Damco Logistics', style)
            sheet.write(row_num, 4, work.booking_no, style)
            sheet.write(row_num, 5, 'DAMCO ' + year + ' V.WK.' + week, style)
            sheet.write(row_num, 6, '', style)
            sheet.write(row_num, 7, work.container_no, style)
            sheet.write(row_num, 8, work.size, style)
            sheet.write(row_num, 9, 1, style)
            sheet.write(row_num, 10, drayage, style_currency)
            sheet.write(row_num, 11, 0, style_currency)
            sheet.write(row_num, 12, 0, style_currency)
            sheet.write(row_num, 13, 0, style_currency)
            sheet.write(row_num, 14, 0, style_currency)
            sheet.write(row_num, 15, 0, style_currency)
            sheet.write(row_num, 16, 0, style_currency)
            sheet.write(row_num, 17, 0, style_currency)
            sheet.write(row_num, 18, 0, style_currency)
            sheet.write(row_num, 19, xlwt.Formula("SUM(K" + num + ":S" + num + ")"), style_currency)

        for row in range(8 - len(invoice_details)):
            row_num += 1
            for col in range(0, 10):
                sheet.write(row_num, col, '', style)
            for col in range(10, 20):
                sheet.write(row_num, col, '', style_currency)


        # Total
        style = xlwt.XFStyle()
        style.borders = style_xls.border_all()
        style.font = style_xls.font_size_20_bold()

        style_blank = copy.deepcopy(style)
        style_head = copy.deepcopy(style)
        style_currency = copy.deepcopy(style)

        style.alignment = style_xls.align_center()

        style_blank.pattern = style_xls.bg_light_gray()

        style_head.pattern = style_xls.bg_light_green()
        style_head_i = copy.deepcopy(style_head)
        style_head_i.font = style_xls.font_size_20_i()
        style_head_i.alignment = style_xls.align_center()

        style_currency.alignment = style_xls.align_right()
        style_currency.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        style_currency_i = copy.deepcopy(style_currency)
        style_currency_i.font = style_xls.font_size_20_i()

        sheet.write_merge(21, 21, 7, 8, 'Total (Before Vat)', style_head)
        sheet.write(21, 9, xlwt.Formula("SUM(J13:J20)"), style)

        row_num = 21
        for item in ['1I', '1J', '1E', '1F']:
            row_num += 1
            sheet.write_merge(row_num, row_num, 7, 8, '', style_head_i)
            sheet.write(row_num, 9, item, style_head_i)

        sheet.write_merge(26, 26, 7, 8, 'VAT 7%', style_head)
        sheet.write(26, 9, '', style_head)

        sheet.write_merge(27, 27, 7, 8, 'Total (After VAT)', style_head)
        sheet.write(27, 9, xlwt.Formula("SUM(J13:J20)"), style)

        sheet.write_merge(28, 28, 7, 8, 'WHT x%', style_head)
        sheet.write(28, 9, '', style_head)

        sheet.write_merge(29, 29, 7, 8, 'WHT Code', style_head)
        sheet.write(29, 9, '', style_head)

        sheet.write_merge(30, 30, 7, 8, 'Total (After WHT)', style_head)
        sheet.write(30, 9, '', style_head)

        sheet.write(21, 10, xlwt.Formula("ROUND(SUM(K13:K20),1)"), style_currency)
        sheet.write(21, 11, xlwt.Formula("ROUND(SUM(L13:L20),1)"), style_currency)
        sheet.write(21, 12, xlwt.Formula("SUM(M13:M20)"), style_currency)
        sheet.write(21, 13, xlwt.Formula("SUM(N13:N20)"), style_currency)
        sheet.write(21, 14, xlwt.Formula("SUM(O13:O20)"), style_currency)
        sheet.write(21, 15, xlwt.Formula("ROUND(SUM(P13:P20),1)"), style_currency)
        sheet.write(21, 16, xlwt.Formula("ROUND(SUM(Q13:Q20),2)"), style_currency)
        sheet.write(21, 17, xlwt.Formula("ROUND(SUM(R13:R20),1)"), style_currency)
        sheet.write(21, 18, xlwt.Formula("ROUND(SUM(S13:S20),1)"), style_currency)
        sheet.write(21, 19, xlwt.Formula("SUM(K22:S22)"), style_currency)

        sheet.write(22, 10, xlwt.Formula("K22"), style_currency_i)
        sheet.write(22, 11, xlwt.Formula("L22"), style_currency_i)
        for col in range(12, 19):
            sheet.write(22, col, '', style_blank)
        sheet.write(22, 19, xlwt.Formula("SUM(K23:S23)"), style_currency_i)

        for col in range(10, 16):
            sheet.write(23, col, '', style_blank)
        sheet.write(23, 16, xlwt.Formula("ROUND(Q22*107%,1)"), style_currency_i)
        sheet.write(23, 17, xlwt.Formula("ROUND(R22*107%,1)"), style_currency_i)
        sheet.write(23, 18, xlwt.Formula("ROUND(S22*107%,1)"), style_currency_i)
        sheet.write(23, 19, xlwt.Formula("SUM(K24:S24)"), style_currency_i)

        sheet.write(24, 10, '', style_blank)
        sheet.write(24, 11, '', style_blank)
        sheet.write(24, 12, xlwt.Formula("M22"), style_currency_i)
        sheet.write(24, 13, xlwt.Formula("N22"), style_currency_i)
        sheet.write(24, 14, xlwt.Formula("O22"), style_currency_i)
        for col in range(15, 19):
            sheet.write(24, col, '', style_blank)
        sheet.write(24, 19, xlwt.Formula("SUM(K25:S25)"), style_currency_i)

        for col in range(10, 15):
            sheet.write(25, col, '', style_blank)
        sheet.write(25, 15, xlwt.Formula("P22"), style_currency_i)
        for col in range(16, 19):
            sheet.write(25, col, '', style_blank)
        sheet.write(25, 19, xlwt.Formula("SUM(K26:S26)"), style_currency_i)

        sheet.write(26, 10, '', style_blank)
        sheet.write(26, 11, '', style_blank)
        sheet.write(26, 12, xlwt.Formula("ROUND(M22*7%,2)"), style_currency)
        sheet.write(26, 13, xlwt.Formula("ROUND(N22*7%,2)"), style_currency)
        sheet.write(26, 14, xlwt.Formula("ROUND(O22*7%,2)"), style_currency)
        sheet.write(26, 15, xlwt.Formula("ROUND(P22*7%,1)"), style_currency)
        for col in range(16, 19):
            sheet.write(26, col, '', style_blank)
        sheet.write(26, 19, xlwt.Formula("SUM(K27:S27)"), style_currency)

        sheet.write(27, 10, xlwt.Formula("SUM(K23:K27)"), style_currency)
        sheet.write(27, 11, xlwt.Formula("SUM(L23:L27)"), style_currency)
        sheet.write(27, 12, xlwt.Formula("ROUND(SUM(M23:M27),0)"), style_currency)
        sheet.write(27, 13, xlwt.Formula("ROUND(SUM(N23:N27),0)"), style_currency)
        sheet.write(27, 14, xlwt.Formula("ROUND(SUM(O23:O27),0)"), style_currency)
        sheet.write(27, 15, xlwt.Formula("SUM(P23:P27)"), style_currency)
        sheet.write(27, 16, xlwt.Formula("SUM(Q23:Q27)"), style_currency)
        sheet.write(27, 17, xlwt.Formula("SUM(R23:R27)"), style_currency)
        sheet.write(27, 18, xlwt.Formula("SUM(S23:S27)"), style_currency)
        sheet.write(27, 19, xlwt.Formula("SUM(K28:S28)"), style_currency)

        sheet.write(28, 10, xlwt.Formula("ROUND(K22*1%,1)"), style_currency)
        sheet.write(28, 11, xlwt.Formula("ROUND(L22*1%,1)"), style_currency)
        for col in range(12, 15):
            sheet.write(28, col, '', style_blank)
        sheet.write(28, 15, xlwt.Formula("ROUND(P22*3%,1)"), style_currency)
        for col in range(16, 19):
            sheet.write(28, col, '', style_blank)
        sheet.write(28, 19, xlwt.Formula("SUM(K29:S29)"), style_currency)
        
        style_head.alignment = style_xls.align_center()
        sheet.write(29, 10, 'A1', style_head)
        sheet.write(29, 11, 'A1', style_head)
        for col in range(12, 15):
            sheet.write(29, col, '', style_head)
        sheet.write(29, 15, 'J1', style_head)
        for col in range(16, 20):
            sheet.write(29, col, '', style_head)

        sheet.write(30, 10, xlwt.Formula("K28-K29"), style_currency)
        sheet.write(30, 11, xlwt.Formula("L28-L29"), style_currency)
        sheet.write(30, 12, xlwt.Formula("M28-M29"), style_currency)
        sheet.write(30, 13, xlwt.Formula("N28-N29"), style_currency)
        sheet.write(30, 14, xlwt.Formula("O28-O29"), style_currency)
        sheet.write(30, 15, xlwt.Formula("P28-P29"), style_currency)
        sheet.write(30, 16, xlwt.Formula("Q28-Q29"), style_currency)
        sheet.write(30, 17, xlwt.Formula("R28-R29"), style_currency)
        sheet.write(30, 18, xlwt.Formula("S28-S29"), style_currency)
        sheet.write(30, 19, xlwt.Formula("SUM(K31:S31)"), style_currency)


        # Footer
        style = xlwt.XFStyle()
        style.borders = style_xls.border_bottom()

        for col in range(12, 20):
            sheet.write(31, col, '', style)

        style.font = style_xls.font_size_26_bold()
        style.borders = style_xls.border_left()
        style.alignment = style_xls.align_center()

        sheet.write(32, 12, 'ผู้วางบิล', style)
        sheet.write(32, 16, 'ผู้รับวางบิล', style)

        style.font = style_xls.font_size_26()
        sheet.write(33, 12, 'ลงชื่อ', style)
        sheet.write(33, 16, 'ลงชื่อ', style)

        sheet.write(34, 12, 'วันที่', style)
        sheet.write(34, 16, 'วันที่', style)

        style.borders = style_xls.border_left_bottom()
        sheet.write(35, 12, '', style)
        sheet.write(35, 16, '', style)

        style.borders = style_xls.border_y()
        for col in range(13, 16):
            sheet.write(34, col, '', style)
            sheet.write(35, col, '', style)

        for col in range(17, 19):
            sheet.write(34, col, '', style)
            sheet.write(35, col, '', style)

        style.borders = style_xls.border_right()
        sheet.write(32, 19, '', style)
        
        style.borders = style_xls.border_right_bottom()
        for row in range(33, 36):
            sheet.write(row, 19, '', style)

        wb.save(response)
        return response
    return False
