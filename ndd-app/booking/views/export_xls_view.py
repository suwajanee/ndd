# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

import xlwt

from ..models import Booking
from .utils import StyleXls
from agent_transport.models import AgentTransport
from customer.models import Principal, Shipper


@login_required(login_url=reverse_lazy('login'))
def export_page(request):
    return render(request, 'export.html', {'nbar': 'export-page'})

def export_xls(request):
    if request.method == 'POST':
        date_from = request.POST['date_from']
        date_to = request.POST['date_to']

        from_date = datetime.strptime(date_from, '%Y-%m-%d')
        to_date = datetime.strptime(date_to, '%Y-%m-%d')
        file_name = from_date.strftime('%d %b %y') + ' - ' + to_date.strftime('%d %b %y')

        filter_data = {
            'date__gte': date_from,
            'date__lte': date_to
        }

        style_xls = StyleXls()

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="Booking (' + file_name + ').xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        ws_booking = wb.add_sheet('Booking')
        
        ws_booking.col(0).width = 250*10
        ws_booking.col(1).width = 250*11
        ws_booking.col(2).width = 250*7
        ws_booking.col(3).width = 250*32
        ws_booking.col(4).width = 250*11
        ws_booking.col(5).width = 250*11
        ws_booking.col(6).width = 250*20
        ws_booking.col(7).width = 250*11
        ws_booking.col(8).width = 250*12
        ws_booking.col(9).width = 250*11
        ws_booking.col(10).width = 250*12
        ws_booking.col(11).width = 250*11
        ws_booking.col(12).width = 250*11
        ws_booking.col(13).width = 250*12
        ws_booking.col(14).width = 250*20
        ws_booking.col(15).width = 250*20
        ws_booking.col(16).width = 250*15
        ws_booking.col(17).width = 250*20
        ws_booking.col(18).width = 250*11
        ws_booking.col(19).width = 250*11
        ws_booking.col(20).width = 250*10
        ws_booking.col(21).width = 250*20
        ws_booking.col(22).width = 250*15
        ws_booking.col(23).width = 250*11
        ws_booking.col(24).width = 250*11
        ws_booking.col(25).width = 250*11

        # Sheet header
        style = style_xls.header_style()

        ws_booking.row(0).height_mismatch = True
        ws_booking.row(0).height = 20*25

        columns = ['Time', 'Date', 'Principal', 'Shipper', 'Agent', 'Size', 'Booking', 'TR', 'FM', 'TR', 'Factory', 'TR', 'TR', 'To', 'Container', 'Seal no', 'Tare', \
        'Vessel', 'Port', 'Closing date', 'Closing time', 'Remark', 'Work ID', 'Pick up', 'Factory', 'Return']

        for col_num in range(len(columns)):
            if col_num == 25:
                ws_booking.write_merge(0, 0, 25, 26, columns[col_num], style)
            else:
                ws_booking.write(0, col_num, columns[col_num], style)

        # Sheet body, remaining rows
        rows = Booking.objects.filter(**filter_data).values_list('time', 'date', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'pickup_tr', 'pickup_from', 'forward_tr', \
        'factory', 'backward_tr', 'return_tr', 'return_to', 'container_no', 'seal_no', 'tare', 'vessel', 'port', 'closing_date', 'closing_time', 'remark', 'work_id', \
        'pickup_date', 'factory_date', 'return_date', 'yard_ndd', 'fac_ndd', 'nextday', 'status', 'detail').order_by('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')

        row_num = 0
        row_prev = None
        booking_prev = None
        booking_index = -1
        for row in rows:
            row = list(row)
            bg_black = False 
            row_num += 1
            ws_booking.row(row_num).height_mismatch = True
            ws_booking.row(row_num).height = 20*25

            if row_prev != None and row_prev != row[1]:
                style = style_xls.bg_black()
                ws_booking.write_merge(row_num, row_num, 0, len(row)-5, '', style)
                row_num += 1
                ws_booking.row(row_num).height_mismatch = True
                ws_booking.row(row_num).height = 20*25
            row_prev = row[1]

            for col_num in range(len(row)-4):
                style = xlwt.XFStyle()
                style.borders = style_xls.border_cell()
                style.alignment = style_xls.align_center()

                if not row[len(row)-1]: 
                    row[len(row)-1] = {}

                if col_num == 0:
                    if 'time' in row[len(row)-1]:
                        index = int(row[len(row)-1]['time'])-1
                        style.pattern = style_xls.bg_time(index)
                    try:
                        time = row[col_num].split('.')
                        if int(time[0])>2 and int(time[0])<10:
                            style.pattern = style_xls.bg_yellow()
                    except:
                        pass

                if col_num == 2:
                    style.alignment = style_xls.align_left()
                    if 'print' in row[len(row)-1]:
                        style.pattern = style_xls.bg_bright_green()

                    try:
                        row[col_num] = Principal.objects.get(pk=row[col_num]).name
                    except Principal.DoesNotExist:
                        row[col_num] = ''

                if col_num == 3:
                    style.alignment = style_xls.align_left()
                    try:
                        row[col_num] = Shipper.objects.get(pk=row[col_num]).name
                    except Shipper.DoesNotExist:
                        row[col_num] = ''

                if col_num == 14 or col_num == 15:
                    style.font = style_xls.font_bold()
                    if 'container_no' in row[len(row)-1] and col_num == 14:
                        index = int(row[len(row)-1]['container_no'])-1
                        style.pattern = style_xls.bg_container_seal(index)
                    elif 'seal_no' in row[len(row)-1] and col_num == 15:
                        index = int(row[len(row)-1]['seal_no'])-1
                        style.pattern = style_xls.bg_container_seal(index)
                    
                if str(type(row[col_num])) == "<class 'datetime.date'>" :
                    style.num_format_str = 'dd/mm/yy'

                if col_num > 22 and col_num < 27:
                    if row[len(row)-3] == '1':
                        style.pattern = style_xls.bg_turquoise()
                    elif row[len(row)-3] == '2':
                        style.pattern = style_xls.bg_aqua()
                
                if booking_prev != row[6]:
                    if booking_index > 8:
                        booking_index = -1
                    booking_index += 1
                booking_prev = row[6]

                if col_num == 6:
                    style.pattern = style_xls.bg_booking(booking_index)

                if col_num == 21:
                    style.alignment = style_xls.align_left()

                if col_num in [7, 9, 11, 12]:
                    if row[col_num] != '':
                        style.pattern = style_xls.bg_sky_blue()

                    if (col_num == 7 and row[len(row)-5] in ['1', '2']) or (col_num == 11 and row[len(row)-4] in ['1', '3']):
                        style.pattern = style_xls.bg_yellow() 
                        
                    if row[len(row)-2] == '3' and col_num == 7:
                        style.pattern = style_xls.bg_bright_green()
                    elif row[len(row)-2] == '4' and col_num in [7, 9]:
                        style.pattern = style_xls.bg_bright_green()
                    elif row[len(row)-2] == '5' and col_num in [7, 9 ,11]:
                        style.pattern = style_xls.bg_bright_green()
                    elif row[len(row)-2] == '2':
                        style.pattern = style_xls.bg_bright_green()
                        if 'morning_work' in row[len(row)-1] and col_num == 12:
                            index = int(row[len(row)-1]['morning_work'])-1
                            style.pattern = style_xls.bg_count(index)
                                       
                if row[len(row)-2] == '0':
                    style.pattern = style_xls.cancel_row()
                    
                if col_num == 26:
                    if 'return_time' in row[len(row)-1]:
                        return_time = row[len(row)-1]['return_time']
                    else:
                        return_time = ''
                    ws_booking.write(row_num, col_num, return_time, style)

                else:
                    ws_booking.write(row_num, col_num, row[col_num], style)


        ws_agent_transport = wb.add_sheet('สายเรือ')

        ws_agent_transport.col(0).width = 250*20
        ws_agent_transport.col(1).width = 250*11
        ws_agent_transport.col(2).width = 250*7
        ws_agent_transport.col(3).width = 250*32
        ws_agent_transport.col(4).width = 250*11
        ws_agent_transport.col(5).width = 250*11
        ws_agent_transport.col(6).width = 250*20
        ws_agent_transport.col(7).width = 250*11
        ws_agent_transport.col(8).width = 250*12
        ws_agent_transport.col(9).width = 250*11
        ws_agent_transport.col(10).width = 250*12
        ws_agent_transport.col(11).width = 250*20
        ws_agent_transport.col(12).width = 250*20
        ws_agent_transport.col(13).width = 250*20
        ws_agent_transport.col(14).width = 250*15
        ws_agent_transport.col(15).width = 250*11
        ws_agent_transport.col(16).width = 250*11


        # Sheet header
        style = style_xls.header_style()

        ws_agent_transport.row(0).height_mismatch = True
        ws_agent_transport.row(0).height = 20*25

        columns = [' ', 'Date', 'Principal', 'Shipper', 'Agent', 'Size', 'Booking', 'TR', 'FM', 'TR', 'TO', 'Container 1', 'Container 2', \
            'Remark', 'Work ID', 'Pick up', 'Return']

        for col_num in range(len(columns)):
            ws_agent_transport.write(0, col_num, columns[col_num], style)

        # Sheet body, remaining rows
        rows = AgentTransport.objects.filter(**filter_data).values_list('operation_type', 'date', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'pickup_tr', 'pickup_from','return_tr', 'return_to', \
        'container_1', 'container_2', 'remark', 'work_id', 'pickup_date', 'return_date', 'yard_ndd', 'work_type', 'price', 'status', 'detail').order_by('date', 'principal__name', 'shipper__name', 'work_type', 'operation_type', \
        Case(When(work_type='ep', then='booking_no'),), 'work_id')

        row_num = 0
        row_prev = None
        booking_prev = None
        booking_index = -1
        for row in rows:
            row = list(row)
            bg_black = False 
            row_num += 1
            ws_agent_transport.row(row_num).height_mismatch = True
            ws_agent_transport.row(row_num).height = 20*25

            if row_prev != None:
                try:
                    row[3] = Shipper.objects.get(pk=row[3]).name
                except Shipper.DoesNotExist:
                    row[3] = ''

                if row_prev[0] != row[0] or row_prev[1] != row[1] or row_prev[3] != row[3] or row_prev[len(row)-4] != row[len(row)-4]:
                    style = style_xls.bg_black()
                    ws_agent_transport.write_merge(row_num, row_num, 0, len(row)-6, '', style)
                    row_num += 1
                    ws_agent_transport.row(row_num).height_mismatch = True
                    ws_agent_transport.row(row_num).height = 20*25

            row_prev = row

            for col_num in range(len(row)-5):
                style = xlwt.XFStyle()
                style.borders = style_xls.border_cell()
                style.alignment = style_xls.align_center()

                if not row[len(row)-1]: 
                    row[len(row)-1] = {}

                if col_num == 2:
                    style.alignment = style_xls.align_left()
                    if 'print' in row[len(row)-1]:
                        style.pattern = style_xls.bg_bright_green()

                    try:
                        row[col_num] = Principal.objects.get(pk=row[col_num]).name
                    except Principal.DoesNotExist:
                        row[col_num] = ''

                if col_num == 3 or col_num == 13:
                    style.alignment = style_xls.align_left()

                if col_num == 11 or col_num == 12:
                    style.font = style_xls.font_bold()
                    if 'container_1' in row[len(row)-1] and col_num == 11:
                        index = int(row[len(row)-1]['container_1'])-1
                        style.pattern = style_xls.bg_container_seal(index)
                    elif 'container_2' in row[len(row)-1] and col_num == 12:
                        index = int(row[len(row)-1]['container_2'])-1
                        style.pattern = style_xls.bg_container_seal(index)

                if str(type(row[col_num])) == "<class 'datetime.date'>" :
                    style.num_format_str = 'dd/mm/yy'

                if booking_prev != row[6]:
                    if booking_index > 8:
                        booking_index = -1
                    booking_index += 1
                booking_prev = row[6]

                if col_num == 6:
                    style.pattern = style_xls.bg_booking(booking_index)

                if col_num == 7 or col_num == 9:
                    if row[col_num] != '':
                        style.pattern = style_xls.bg_sky_blue()

                    if col_num == 7 and row[len(row)-5] in ['1', '2']:
                        style.pattern = style_xls.bg_yellow() 

                    if row[len(row)-2] == '3' and col_num == 7:
                        style.pattern = style_xls.bg_bright_green()
                    elif row[len(row)-2] in ['4', '2'] and col_num in [7, 9]:
                        style.pattern = style_xls.bg_bright_green()
                        if 'morning_work' in row[len(row)-1] and row[len(row)-2] == '2' and col_num == 9:
                            index = int(row[len(row)-1]['morning_work'])-1
                            style.pattern = style_xls.bg_count(index)

                if row[len(row)-2] == '0':
                    style.pattern = style_xls.cancel_row()

                if col_num == 0:
                    if row[col_num] == 'export_loaded':
                        operation = 'ตู้หนักไป'
                    elif  row[col_num] == 'import_loaded':
                        operation = 'ตู้หนักกลับ'
                    elif  row[col_num] == 'export_empty':
                        operation = 'ตู้เปล่าไป'
                    elif  row[col_num] == 'import_empty':
                        operation = 'ตู้เปล่ากลับ'

                    ws_agent_transport.write(row_num, col_num, '**' + operation + ' ' + str(row[len(row)-3]) + '**', style)
                else:
                    ws_agent_transport.write(row_num, col_num, row[col_num], style)

        wb.save(response)
        return response
    return False

