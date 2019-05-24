# -*- coding: utf-8 -*-

from django.db.models import Case, When
from django.db.models import Q
from django.http import HttpResponse

import xlwt

from ..models import Booking
from ..models import BookingTime
from .utils import StyleXls
from customer.models import Principal, Shipper


def export_time(request):
    if request.method == "POST":
        customer_id = request.POST['customer']
        shipper_id = request.POST['shipper']
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']

        style_xls = StyleXls()

        try:
            customer = Principal.objects.get(pk=customer_id)
        except Principal.DoesNotExist:
            customer = ''

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="' + customer.name + '_Time.xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        sheet = wb.add_sheet('Time')

        # Col width
        sheet.col(0).width = 250*12
        sheet.col(1).width = 250*7
        sheet.col(2).width = 250*32
        sheet.col(3).width = 250*11
        sheet.col(4).width = 250*11
        sheet.col(5).width = 250*20
        sheet.col(6).width = 250*11
        sheet.col(7).width = 250*12
        sheet.col(8).width = 250*11
        sheet.col(9).width = 250*12
        sheet.col(10).width = 250*11
        sheet.col(11).width = 250*11
        sheet.col(12).width = 250*12
        sheet.col(13).width = 250*20
        sheet.col(14).width = 250*20
        sheet.col(15).width = 250*15
        for x in range(16, 24):
            sheet.col(x).width = 250*8

        # Sheet header
        style = style_xls.header_style()

        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 20*25

        sheet.row(1).height_mismatch = True
        sheet.row(1).height = 20*25

        columns = ['Date', 'Principal', 'Shipper', 'Agent', 'Size', 'Booking', 'TR', 'FM', 'TR', 'Factory', 'TR', 'TR', 'To', 'Container', 'Seal no','Work ID', \
                    'In', 'Out', 'In', 'Start', 'Finish', 'Out', 'In', 'Out']

        sheet.write_merge(0, 0, 16, 17, 'Pick up', style)
        sheet.write_merge(0, 0, 18, 21, 'Factory', style)
        sheet.write_merge(0, 0, 22, 23, 'Return', style)

        for col_num in range(len(columns)):
            if col_num <= 15 :
                sheet.write_merge(0, 1, col_num, col_num, columns[col_num], style)
            else:
                sheet.write(1, col_num, columns[col_num], style)

        filter_data = {
            'principal': customer,
            'date__lte': date_to,
            'date__gte': date_from
        }

        if shipper_id:
            filter_data['shipper__pk'] = shipper_id

        rows = Booking.objects.filter(**filter_data).values_list('date', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'pickup_tr', 'pickup_from', 'forward_tr', \
                'factory', 'backward_tr', 'return_tr', 'return_to', 'container_no', 'seal_no', 'work_id', 'pk').order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')
 
        row_prev = None
        booking_prev = None
        booking_index = -1
        row_num = 1

        for row in rows:
            row = list(row)
            row_num += 1
            sheet.row(row_num).height_mismatch = True
            sheet.row(row_num).height = 20*27

            if row_prev != None and row_prev != row[0]:
                style = style_xls.bg_black()
                sheet.write_merge(row_num, row_num, 0, 23, '', style)
                row_num += 1
                sheet.row(row_num).height_mismatch = True
                sheet.row(row_num).height = 20*27
            row_prev = row[0]

            for col_num in range(len(row)-1):
                style = xlwt.XFStyle()
                style.borders = style_xls.border_cell()
                style.alignment = style_xls.align_center()

                if col_num == 0 or col_num == 1 or col_num == 2 or col_num == 4 or col_num == 5:
                    if str(type(row[col_num])) == "<class 'datetime.date'>" :
                        style.num_format_str = 'dd/mm/yy'
                    
                    if col_num == 1:
                        style.alignment = style_xls.align_left()
                        row[col_num] = customer.name

                    if col_num == 2:
                        style.alignment = style_xls.align_left()
                        try:
                            row[col_num] = Shipper.objects.get(pk=row[col_num]).name
                        except Shipper.DoesNotExist:
                            row[col_num] = ''

                    if col_num == 4:
                        if not 'X' in row[col_num]:
                            row[col_num] = '1X' + row[col_num]

                    if booking_prev != row[5]:
                        if booking_index > 8:
                            booking_index = -1
                        booking_index += 1
                    booking_prev = row[5]

                    if col_num == 5:
                        style.pattern = style_xls.bg_booking(booking_index)

                sheet.write(row_num, col_num, row[col_num], style)

            row_time = BookingTime.objects.filter(booking__pk=row[16]).values_list('pickup_in_time', 'pickup_out_time', 'factory_in_time', 'factory_load_start_time', \
                        'factory_load_finish_time', 'factory_out_time', 'return_in_time', 'return_out_time')

            if len(row_time):
                row_time = row_time[0]
                
                for col_time in range(len(row_time)):
                    if row_time[col_time]['time']:
                        style.pattern = style_xls.bg_bright_green()
                    else:
                        style.pattern = style_xls.bg_none()
                    sheet.write(row_num, col_time + 16, row_time[col_time]['time'], style)

            else:
                for col_time in range(16, 24):
                    sheet.write(row_num, col_time, "", style)

        wb.save(response)
        return response
    return False


