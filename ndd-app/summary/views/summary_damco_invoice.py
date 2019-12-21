# -*- coding: utf-8 -*-

import copy

from django.http import HttpResponse

import xlwt

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
        sheet.col(0).width = 256*11
        sheet.col(1).width = 256*14
        sheet.col(2).width = 256*19
        sheet.col(3).width = 256*27
        sheet.col(4).width = 256*25
        sheet.col(5).width = 256*25
        sheet.col(6).width = 256*41
        sheet.col(7).width = 256*19
        sheet.col(8).width = 256*10
        sheet.col(9).width = 256*10
        sheet.col(10).width = 256*18
        sheet.col(11).width = 256*18
        sheet.col(12).width = 256*13
        sheet.col(13).width = 256*14
        sheet.col(14).width = 256*19
        sheet.col(15).width = 256*16
        sheet.col(16).width = 256*17
        sheet.col(17).width = 256*17
        sheet.col(18).width = 256*15
        sheet.col(19).width = 256*20

        # Row height
        for row in range(0, 8):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 645
        sheet.row(8).height_mismatch = True
        sheet.row(8).height = 270

        sheet.row(9).height_mismatch = True
        sheet.row(9).height = 1050
        sheet.row(10).height_mismatch = True
        sheet.row(10).height = 525
        sheet.row(11).height_mismatch = True
        sheet.row(11).height = 525

        for row in range(12, 23):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 20*30

        sheet.row(23).height_mismatch = True
        sheet.row(23).height = 495
        for row in range(24, 34):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 20*36
        sheet.row(34).height_mismatch = True
        sheet.row(34).height = 495
        for row in range(35, 39):
            sheet.row(row).height_mismatch = True
            sheet.row(row).height = 525
        

        # Header invoice
        style = xlwt.XFStyle()
        style.font = style_xls.font_size_22_bold()
        
        sheet.write_merge(6, 6, 1, 7, '0105534075332 หรือ 0105553066823', style)

        style.alignment = style_xls.align_center()
        sheet.write_merge(0, 0, 0, 19, 'N&DD INTERNATIONAL (THAILAND) CO.,LTD.', style)
        sheet.write_merge(1, 1, 0, 19, '10/19 MOO.4 BANGCHALONG SUBDISTRICT BANGPLEE DISTRICT SAMUTPRAKARN 10540 TEL.02-1305977-78 FAX.02-1305979', style)
        sheet.write_merge(3, 3, 16, 19, 'PRE-INVOICE', style)

        style.font = style_xls.font_size_22()
        sheet.write_merge(2, 2, 0, 19, 'เลขประจำตัวผู้เสียภาษี 0105540102061', style)

        style.alignment = style_xls.align_left()
        sheet.write(4, 0, 'ลูกค้า', style)
        sheet.write(5, 0, 'ที่อยู่', style)
        sheet.write(6, 0, 'No.', style)
        sheet.write_merge(4, 4, 1, 7, 'Damco Logistics (Thailand) Co., Ltd. (Head Office)', style)
        sheet.write_merge(5, 5, 1, 7, '1 Empire Tower, South Sathorn Road, Yannawa,  Sathorn Bangkok 10120', style)

        style.borders = style_xls.border_all()
        style.font = style_xls.font_size_20()
        style.alignment = style_xls.align_center()
        sheet.write_merge(4, 4, 16, 17, 'Invoice no.', style)
        sheet.write_merge(5, 5, 16, 17, 'Invoice Date :', style)
        sheet.write_merge(6, 6, 16, 17, 'Kewill no. / Po no.', style)
        style.font = style_xls.font_size_20()
        sheet.write_merge(4, 4, 18, 19, invoice.invoice_no, style)

        style.num_format_str = 'D-MMM-YYYY'
        sheet.write_merge(5, 5, 18, 19, invoice.customer_week.date_billing, style)

        style.num_format_str = 'general'
        style.font = style_xls.font_size_20()
        sheet.write_merge(7, 7, 16, 17, 'Customer Booking no.', style)
        sheet.write_merge(6, 6, 18, 19, '', style)
        sheet.write_merge(7, 7, 18, 19, invoice_details[0].work_normal.booking_no, style)


        # Header table
        style.font = style_xls.font_size_18_bold()
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
        style.font = style_xls.font_size_18()
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
            try:
                drayage = eval(row.drayage_charge['drayage'])
            except:
                drayage = 0
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

        for row in range(11 - len(invoice_details)):
            row_num += 1
            for col in range(0, 10):
                sheet.write(row_num, col, '', style)
            for col in range(10, 20):
                sheet.write(row_num, col, '', style_currency)


        # Total
        style = xlwt.XFStyle()
        style.borders = style_xls.border_all()
        style.font = style_xls.font_size_18_bold()

        style_blank = copy.deepcopy(style)
        style_head = copy.deepcopy(style)
        style_currency = copy.deepcopy(style)

        style.alignment = style_xls.align_center()

        style_blank.pattern = style_xls.bg_light_gray()

        style_head.pattern = style_xls.bg_light_green()
        style_head_i = copy.deepcopy(style_head)
        style_head_i.font = style_xls.font_size_18_i()
        style_head_i.alignment = style_xls.align_center()

        style_currency.alignment = style_xls.align_right()
        style_currency.num_format_str = '_(#,##0.00 ;-#,##0.00 ;"- "_)'
        style_currency_i = copy.deepcopy(style_currency)
        style_currency_i.font = style_xls.font_size_18_i()

        sheet.write_merge(24, 24, 7, 8, 'Total (Before Vat)', style_head)
        sheet.write(24, 9, xlwt.Formula("SUM(J13:J23)"), style)

        row_num = 24
        for item in ['1I', '1J', '1E', '1F']:
            row_num += 1
            sheet.write_merge(row_num, row_num, 7, 8, '', style_head_i)
            sheet.write(row_num, 9, item, style_head_i)

        sheet.write_merge(29, 29, 7, 8, 'VAT 7%', style_head)
        sheet.write(29, 9, '', style_head)

        sheet.write_merge(30, 30, 7, 8, 'Total (After VAT)', style_head)
        sheet.write(30, 9, xlwt.Formula("SUM(J13:J23)"), style)

        sheet.write_merge(31, 31, 7, 8, 'WHT x%', style_head)
        sheet.write(31, 9, '', style_head)

        sheet.write_merge(32, 32, 7, 8, 'WHT Code', style_head)
        sheet.write(32, 9, '', style_head)

        sheet.write_merge(33, 33, 7, 8, 'Total (After WHT)', style_head)
        sheet.write(33, 9, '', style_head)

        sheet.write(24, 10, xlwt.Formula("ROUND(SUM(K13:K23),1)"), style_currency)
        sheet.write(24, 11, xlwt.Formula("ROUND(SUM(L13:L23),1)"), style_currency)
        sheet.write(24, 12, xlwt.Formula("SUM(M13:M23)"), style_currency)
        sheet.write(24, 13, xlwt.Formula("SUM(N13:N23)"), style_currency)
        sheet.write(24, 14, xlwt.Formula("SUM(O13:O23)"), style_currency)
        sheet.write(24, 15, xlwt.Formula("ROUND(SUM(P13:P23),1)"), style_currency)
        sheet.write(24, 16, xlwt.Formula("SUM(Q13:Q23)"), style_currency)
        sheet.write(24, 17, xlwt.Formula("SUM(R13:R23)"), style_currency)
        sheet.write(24, 18, xlwt.Formula("SUM(S13:S23)"), style_currency)
        sheet.write(24, 19, xlwt.Formula("SUM(K25:S25)"), style_currency)

        sheet.write(25, 10, xlwt.Formula("K25"), style_currency_i)
        sheet.write(25, 11, xlwt.Formula("L25"), style_currency_i)
        for col in range(12, 19):
            sheet.write(25, col, '', style_blank)
        sheet.write(25, 19, xlwt.Formula("SUM(K26:S26)"), style_currency_i)

        for col in range(10, 16):
            sheet.write(26, col, '', style_blank)
        sheet.write(26, 16, xlwt.Formula("ROUND(Q25*107%,2)"), style_currency_i)
        sheet.write(26, 17, xlwt.Formula("ROUND(R25*107%,1)"), style_currency_i)
        sheet.write(26, 18, xlwt.Formula("ROUND(S25*107%,1)"), style_currency_i)
        sheet.write(26, 19, xlwt.Formula("SUM(K27:S27)"), style_currency_i)

        sheet.write(27, 10, '', style_blank)
        sheet.write(27, 11, '', style_blank)
        sheet.write(27, 12, xlwt.Formula("M25"), style_currency_i)
        sheet.write(27, 13, xlwt.Formula("N25"), style_currency_i)
        sheet.write(27, 14, xlwt.Formula("O25"), style_currency_i)
        for col in range(15, 19):
            sheet.write(27, col, '', style_blank)
        sheet.write(27, 19, xlwt.Formula("SUM(K28:S28)"), style_currency_i)

        for col in range(10, 15):
            sheet.write(28, col, '', style_blank)
        sheet.write(28, 15, xlwt.Formula("P25"), style_currency_i)
        for col in range(16, 19):
            sheet.write(28, col, '', style_blank)
        sheet.write(28, 19, xlwt.Formula("SUM(K29:S29)"), style_currency_i)

        sheet.write(29, 10, '', style_blank)
        sheet.write(29, 11, '', style_blank)
        sheet.write(29, 12, xlwt.Formula("M25*7%"), style_currency)
        sheet.write(29, 13, xlwt.Formula("N25*7%"), style_currency)
        sheet.write(29, 14, xlwt.Formula("O25*7%"), style_currency)
        sheet.write(29, 15, xlwt.Formula("P25*7%"), style_currency)
        for col in range(16, 19):
            sheet.write(29, col, '', style_blank)
        sheet.write(29, 19, xlwt.Formula("SUM(K30:S30)"), style_currency)

        sheet.write(30, 10, xlwt.Formula("SUM(K26:K30)"), style_currency)
        sheet.write(30, 11, xlwt.Formula("SUM(L26:L30)"), style_currency)
        sheet.write(30, 12, xlwt.Formula("SUM(M26:M30)"), style_currency)
        sheet.write(30, 13, xlwt.Formula("SUM(N26:N30)"), style_currency)
        sheet.write(30, 14, xlwt.Formula("SUM(O26:O30)"), style_currency)
        sheet.write(30, 15, xlwt.Formula("SUM(P26:P30)"), style_currency)
        sheet.write(30, 16, xlwt.Formula("SUM(Q26:Q30)"), style_currency)
        sheet.write(30, 17, xlwt.Formula("SUM(R26:R30)"), style_currency)
        sheet.write(30, 18, xlwt.Formula("SUM(S26:S30)"), style_currency)
        sheet.write(30, 19, xlwt.Formula("SUM(K31:S31)"), style_currency)

        sheet.write(31, 10, xlwt.Formula("ROUND(K25*1%,1)"), style_currency)
        sheet.write(31, 11, xlwt.Formula("ROUND(L25*1%,1)"), style_currency)
        for col in range(12, 15):
            sheet.write(31, col, '', style_blank)
        sheet.write(31, 15, xlwt.Formula("ROUND(P25*3%,1)"), style_currency)
        for col in range(16, 19):
            sheet.write(31, col, '', style_blank)
        sheet.write(31, 19, xlwt.Formula("SUM(K32:S32)"), style_currency)
        
        style_head.alignment = style_xls.align_center()
        sheet.write(32, 10, 'A1', style_head)
        sheet.write(32, 11, 'A1', style_head)
        for col in range(12, 15):
            sheet.write(32, col, '', style_head)
        sheet.write(32, 15, 'J1', style_head)
        for col in range(16, 20):
            sheet.write(32, col, '', style_head)

        sheet.write(33, 10, xlwt.Formula("K31-K32"), style_currency)
        sheet.write(33, 11, xlwt.Formula("L31-L32"), style_currency)
        sheet.write(33, 12, xlwt.Formula("M31-M32"), style_currency)
        sheet.write(33, 13, xlwt.Formula("N31-N32"), style_currency)
        sheet.write(33, 14, xlwt.Formula("O31-O32"), style_currency)
        sheet.write(33, 15, xlwt.Formula("P31-P32"), style_currency)
        sheet.write(33, 16, xlwt.Formula("Q31-Q32"), style_currency)
        sheet.write(33, 17, xlwt.Formula("R31-R32"), style_currency)
        sheet.write(33, 18, xlwt.Formula("S31-S32"), style_currency)
        sheet.write(33, 19, xlwt.Formula("SUM(K34:S34)"), style_currency)


        # Footer
        style = xlwt.XFStyle()
        style.borders = style_xls.border_bottom()

        for col in range(12, 20):
            sheet.write(34, col, '', style)

        style.font = style_xls.font_size_18_bold()
        style.borders = style_xls.border_left()
        style.alignment = style_xls.align_center()

        sheet.write(35, 12, 'ผู้วางบิล', style)
        sheet.write(35, 16, 'ผู้รับวางบิล', style)

        style.font = style_xls.font_size_18()
        sheet.write(36, 12, 'ลงชื่อ', style)
        sheet.write(36, 16, 'ลงชื่อ', style)

        sheet.write(37, 12, 'วันที่', style)
        sheet.write(37, 16, 'วันที่', style)

        style.borders = style_xls.border_left_bottom()
        sheet.write(38, 12, '', style)
        sheet.write(38, 16, '', style)

        style.borders = style_xls.border_y()
        for col in range(13, 16):
            sheet.write(37, col, '', style)
            sheet.write(38, col, '', style)

        for col in range(17, 19):
            sheet.write(37, col, '', style)
            sheet.write(38, col, '', style)

        style.borders = style_xls.border_right()
        sheet.write(35, 19, '', style)
        
        style.borders = style_xls.border_right_bottom()
        for row in range(36, 39):
            sheet.write(row, 19, '', style)

        wb.save(response)
        return response
    return False
