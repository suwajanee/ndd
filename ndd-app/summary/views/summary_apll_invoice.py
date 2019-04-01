# -*- coding: utf-8 -*-

from datetime import datetime
import json
import requests

from django.http import JsonResponse
from django.http import HttpResponse

from bs4 import BeautifulSoup
import xlwt

from ..models import InvoiceSetting
from .utils_apll import StyleXls


def apll_invoice(request):
    if request.method == 'POST':
        pickup_date = request.POST['pickup_date']
        to_date = request.POST['to_date']

        invoice_setting = InvoiceSetting.objects.get(primary='apll')

        login_list = invoice_setting.data['login_url']
        html_list = invoice_setting.data['html_url']

        login = invoice_setting.data['login_data']

        data = {
            'DtpReturnDate': datetime.strptime(pickup_date, '%Y-%m-%d').strftime('%d-%b-%Y').upper(),
            'DtpReturnDate2': datetime.strptime(to_date, '%Y-%m-%d').strftime('%d-%b-%Y').upper(),
            'Vendor': invoice_setting.data['vendor']
        }

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="APLL_Summary.xls"'

        wb = xlwt.Workbook(encoding='utf-8', style_compression=2)
        sheet_1 = wb.add_sheet('APLL CTCI')
        sheet_2 = wb.add_sheet('APLL NON CTCI')
        sheet_3 = wb.add_sheet('APLL NON CTCI CNS (IN)')
        sheet_4 = wb.add_sheet('APLL NON CTCI CNS')

        sheet_list = [sheet_1, sheet_2, sheet_3, sheet_4]

        url = []

        style_xls = StyleXls()

        columns = ['Item', 'Work Order', 'Customer Name', 'Vessel/Truck Routing', '', 'Pick Up/Return Date', 'Pick Up/Return Date', 'Booking No.', \
                    'Container No.', 'Size', 'drayage charge', 'Gate charge pickup empty(if any)', 'Gate charge laden return', 'Weight Charge', \
                    'Gate charge drop empty', 'TTL Charge', 'Doc No.', 'Can\'t Claim Amount', 'Amount', 'Vat', 'Remark']

        table_header_style = style_xls.table_header_style()
        title_style = style_xls.title_style()

        header_blue = style_xls.header_blue(False)
        header_blue_20 = style_xls.header_blue(True)
        header_rose = style_xls.header_rose(False)
        header_rose_20 = style_xls.header_rose(True)

        std_style = style_xls.std_style(False, 2)
        std_left_style = style_xls.std_style(False, 0)
        std_currency_style = style_xls.std_style(False, 1)

        total_style = style_xls.std_style(True, 2)
        total_currency_style = style_xls.std_style(True, 1)

        total_list = []
        for index, sheet in enumerate(sheet_list):
            # Col width
            sheet.col(0).width = 250*5
            sheet.col(1).width = 250*14
            sheet.col(2).width = 250*53
            sheet.col(3).width = 250*31
            sheet.col(4).width = 250*50
            sheet.col(5).width = 250*15
            sheet.col(6).width = 250*15
            sheet.col(7).width = 250*23
            sheet.col(8).width = 250*23
            sheet.col(9).width = 250*5
            sheet.col(10).width = 250*17
            sheet.col(11).width = 250*7
            sheet.col(12).width = 250*7
            sheet.col(13).width = 250*7
            sheet.col(14).width = 250*7
            sheet.col(15).width = 250*7
            sheet.col(16).width = 250*15
            sheet.col(17).width = 250*15
            sheet.col(18).width = 250*15
            sheet.col(19).width = 250*15
            sheet.col(20).width = 250*15

            for row in range(0, 1):
                sheet.row(row).height_mismatch = True
                sheet.row(row).height = 20*28

            sheet.write(0, 2, sheet.name, title_style)

            sheet.write(1, 1, 'Invoice', header_blue)
            sheet.write(1, 2, '', header_blue_20)
            sheet.write(1, 3, 'Q', header_rose)
            sheet.write(1, 4, '', header_rose_20)

            for row in range(2, 6):
                sheet.row(row).height_mismatch = True
                sheet.row(row).height = 20*20

            sheet.write_merge(2, 3, 16, 19, 'Reimburement for Gate Charge and Liting Charge', table_header_style)
            sheet.write_merge(4, 4, 18, 19, 'Claim Vat', table_header_style)

            for col_num in range(len(columns)):                
                if col_num == 16 or col_num == 17:
                    sheet.write_merge(4, 5, col_num, col_num, columns[col_num], table_header_style)
                elif col_num == 18 or col_num == 19:
                    sheet.write(5, col_num, columns[col_num], table_header_style)
                else:
                    sheet.write_merge(2, 5, col_num, col_num, columns[col_num], table_header_style)


            login_url = login_list[index]
            html_url = html_list[index]

            rows_total = []
            row_num = 6
            for html in html_url:
                with requests.Session() as session:
                    post = session.post(login_url, data=login)
                    r = session.post(html, data=data)
                    r.encoding = 'utf-8'

                soup = BeautifulSoup(r.content, "html.parser")

                table = soup.find_all('table')[2]
                
                rows = table.find_all('tr', {'bgcolor': None})
                
                from_row = str(row_num + 1)

                if rows:
                    for row_index, row in enumerate(rows):

                        cols = row.find_all('td')
                        
                        sheet.write(row_num, 0, row_index + 1, std_style)
                        sheet.write(row_num, 1, cols[1].text, std_style)
                        sheet.write(row_num, 2, cols[2].text, std_left_style)

                        text = cols[3].text.strip().split('\n')
                        sheet.write(row_num, 3, text[0].strip(), std_style)

                        sheet.write(row_num, 4, '', std_style)

                        text = cols[4].text.strip().split('\n')
                        sheet.write(row_num, 5, text[0].strip(), std_style)
                        sheet.write(row_num, 6, text[1].strip(), std_style)

                        sheet.write(row_num, 7, cols[5].text.strip(), std_style)
                        sheet.write(row_num, 8, cols[6].text.strip(), std_style)
                        sheet.write(row_num, 9, cols[7].text, std_style)

                        text = float(cols[8].text.replace(',', ''))
                        sheet.write(row_num, 10, text, std_currency_style)

                        for col in range(11, 17):
                            sheet.write(row_num, col, '', std_style)

                        sheet.write(row_num, 17, 0, std_currency_style)

                        for col in range(18, 21):
                            sheet.write(row_num, col, '', std_style)

                        sheet.row(row_num).height_mismatch = True
                        sheet.row(row_num).height = 20*29
                        row_num += 1
                else:
                    for col in range(0, 21):
                        sheet.write(row_num, col, '', std_style)
                    row_num += 1
                
                to_row = str(row_num)

                total = {
                    'k': 'SUM(K' + from_row + ':K' + to_row + ')',
                    'r': 'SUM(R' + from_row + ':R' + to_row + ')',
                    's': 'SUM(S' + from_row + ':S' + to_row + ')',
                    't': 'SUM(T' + from_row + ':T' + to_row + ')',
                    'u': 'SUM(U' + from_row + ':U' + to_row + ')',
                }

                for col in range(0, 8):
                    sheet.write(row_num, col, '', total_style)

                sheet.write(row_num, 8, 'Total', total_style)
                sheet.write(row_num, 9, '', total_style)
                sheet.write(row_num, 10, xlwt.Formula(total['k']), total_currency_style)

                for col in range(11, 17):
                    sheet.write(row_num, col, '', total_style)

                sheet.write(row_num, 17, xlwt.Formula(total['r']), total_currency_style)
                sheet.write(row_num, 18, xlwt.Formula(total['s']), total_currency_style)
                sheet.write(row_num, 19, xlwt.Formula(total['t']), total_currency_style)
                sheet.write(row_num, 20, xlwt.Formula(total['u']), total_currency_style)

                sheet.row(row_num).height_mismatch = True
                sheet.row(row_num).height = 20*29
                row_num += 1
                rows_total.append(str(row_num))
            
            total_k = '0'
            for row in rows_total:
                total_k += '+ K' + row

            total_r = total_k.replace('K', 'R')
            total_s = total_k.replace('K', 'S')
            total_t = total_k.replace('K', 'T')
            total_u = total_k.replace('K', 'U')

            for col in range(0, 10):
                sheet.write(row_num, col, '', total_style)

            sheet.write(row_num, 10, xlwt.Formula(total_k), total_currency_style)

            for col in range(11, 17):
                sheet.write(row_num, col, '', total_style)

            sheet.write(row_num, 17, xlwt.Formula(total_r), total_currency_style)
            sheet.write(row_num, 18, xlwt.Formula(total_s), total_currency_style)
            sheet.write(row_num, 19, xlwt.Formula(total_t), total_currency_style)
            sheet.write(row_num, 20, xlwt.Formula(total_u), total_currency_style)

            sheet.row(row_num).height_mismatch = True
            sheet.row(row_num).height = 20*29
            row_num += 1
            g_total = str(row_num)

            for col in range(0, 8):
                sheet.write(row_num, col, '', total_style)

            sheet.write(row_num, 8, 'G.Total', total_style)
            sheet.write(row_num, 9, '', total_style)

            sheet.write(row_num, 10, xlwt.Formula('K' + g_total), total_currency_style)

            for col in range(11, 19):
                sheet.write(row_num, col, '', total_style)

            sheet.write(row_num, 19, xlwt.Formula('SUM(R' + g_total + ':U' + g_total + ')'), total_currency_style)
            
            sheet.write(row_num, 20, '', total_style)

            total_list.append(str(row_num + 1))


        sheet = wb.add_sheet('Total')

        sheet.col(0).width = 250*5
        sheet.col(1).width = 250*25
        sheet.col(2).width = 250*32
        sheet.col(3).width = 250*32
        sheet.col(4).width = 250*16
        sheet.col(5).width = 250*16
        sheet.col(6).width = 250*16
        sheet.col(7).width = 250*18

        head = style_xls.total_page(4)
        std_style = style_xls.total_page(0)
        std_currency_style = style_xls.total_page(1)
        total_style = style_xls.total_page(2)
        total_currency_style = style_xls.total_page(3)

        sheet.write(1, 0, 'Item', head)
        sheet.write(1, 1, 'Job', head)
        sheet.write(1, 2, 'Inv.', head)
        sheet.write(1, 3, 'Q', head)
        sheet.write(1, 4, 'price', head)
        sheet.write(1, 5, 'Gate', head)
        sheet.write(1, 6, 'Other', head)

        row_num = 2
        for index, sheet_name in enumerate(sheet_list):
            link = "'" + sheet_name.name + "'!$"
            row = str(row_num + 1)
            sum_text = 'SUM(E' + row + ':G' + row + ')'

            sheet.write(row_num, 0, index + 1, std_style)
            sheet.write(row_num, 1, sheet_name.name, std_style)
            sheet.write(row_num, 2, xlwt.Formula(link + 'C$2'), std_style)
            sheet.write(row_num, 3, xlwt.Formula(link + 'E$2'), std_style)

            sheet.write(row_num, 4, xlwt.Formula(link + 'K$' + total_list[index]), std_currency_style)
            sheet.write(row_num, 5, xlwt.Formula(link + 'T$' + total_list[index]), std_currency_style)
            sheet.write(row_num, 6, xlwt.Formula(link + 'U$' + total_list[index]), std_currency_style)

            sheet.write(row_num, 7, xlwt.Formula(sum_text), total_currency_style)

            row_num += 1

        sheet.write(6, 1, 'Total', total_style)
        sheet.write(6, 4, xlwt.Formula('SUM(E3:E6)'), total_currency_style)
        sheet.write(6, 5, xlwt.Formula('SUM(F3:F6)'), total_currency_style)
        sheet.write(6, 6, xlwt.Formula('SUM(G3:G6)'), total_currency_style)
        sheet.write(6, 7, xlwt.Formula('SUM(H3:H6)'), total_currency_style)   

        wb.save(response)
        return response
    return False
