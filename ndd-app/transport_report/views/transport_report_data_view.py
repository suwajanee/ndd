# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db.models import FloatField
from django.db.models.functions import Cast
from django.db.models import Func, F, Value
from django.db.models import Sum, Count
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import WorkOrder
from ..models import Expense
from ..models import ExpenseSummaryDate
from ..models import Variable
from ..serializers import WorkOrderSerializer
from ..serializers import ExpenseSerializer
from ..serializers import ExpenseThcSerializer
from ..serializers import ExpenseSummaryDateSerializer
from ..serializers import TruckSerializer
from booking.views.utility.functions import set_if_not_none
from employee.models import Driver
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.serializers import DriverSerializer


# Daily Expense & Daily Driver Expense
@csrf_exempt
def api_get_daily_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":  
            req = json.loads(request.body.decode('utf-8'))
            date = req['date']
            co = req['co']
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except:
                return JsonResponse(False, safe=False)

            report = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__truck__owner=co))
            report = order_expense_report(report)
            serializer = ExpenseSerializer(report, many=True)

            total = report.order_by('work_order__clear_date').aggregate(total=Sum('co_total') + Sum('cus_total'))['total']

            driver_list = get_driver_list(report, co)
            data = {
                'date': date.date(),
                'work_expense': serializer.data,
                'driver_list': driver_list,
                'total': total
            }

            return JsonResponse(data, safe=False)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_daily_driver_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            date = req['date']
            driver_id = req['driver']
            
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
                driver = Employee.objects.get(pk=driver_id)
                driver_serializer = EmployeeSerializer(driver, many=False)
            except:
                return JsonResponse(False, safe=False)

            co = driver.co

            try:
                truck = Driver.objects.get(employee=driver).truck
                truck_serializer = TruckSerializer(truck, many=False)
                truck_data = truck_serializer.data

            except:
                truck_data = {}

            report = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__driver__employee=driver)).order_by('work_order__work_date', 'pk')

            co_report = report.filter(work_order__truck__owner=co)
            not_co_report = report.filter(~Q(work_order__truck__owner=co))

            co_work = ExpenseSerializer(co_report, many=True)
            not_co_work = ExpenseSerializer(not_co_report, many=True)

            total = report.order_by('work_order__clear_date').aggregate(total=Sum('co_total') + Sum('cus_total'))['total']

            data = {
                'driver': driver_serializer.data,
                'truck': truck_data,
                'report': [co_work.data, not_co_work.data],
                'total': total
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


# Expense page & Filter
@csrf_exempt
def api_get_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            page = req['page']
            year = int(req['year'])
            month = int(req['month'])
            period = int(req['period'])
            co = req['co']

            period_num, from_date, to_date = get_from_to_date(co, year, month, period)

            if from_date < to_date:
                expense = Expense.objects.filter(work_order__truck__owner=co)

                expense = expense.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lte=to_date))
                expense = order_expense_report(expense)

                date_list = get_values_list(expense, 'work_order__clear_date')

                expense_serializer = ExpenseThcSerializer(expense, many=True)
                
                pk_list = expense.values_list('pk', flat=True).distinct()

                remark_list = get_values_list(expense, 'work_order__detail__remark')
                customer_list = get_customer_options_filter(expense)

                total_price_list = get_total_price_list(expense)
                total_expense_list = get_total_expense_list(expense)  

                data = {
                    'from_date': from_date,
                    'to_date': to_date,

                    'period': period_num,
                    'report_list': expense_serializer.data,
                    # 'date_list': date_list,

                    'pk_list': list(pk_list),

                    'customer_list': customer_list,
                    'remark_list': ['(empty)'] + remark_list,

                    'total_price_list': total_price_list,
                    # 'total_expense_list': total_expense_list,
                }

                if page == 'expense':
                    data['date_list'] = date_list
                    data['total_expense_list'] = total_expense_list

            else:
                data = {
                    'from_date': None,
                    'to_date': None,

                    'period': 0,
                    'report_list': [],
                    'date_list': [],
                    'pk_list': [],

                    'customer_list': [],
                    'remark_list': [],

                    'total_price_list': [],
                    'total_expense_list': [],
                }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_filter_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            
            page = req['page']
            pk_list = req['pk_list']
            work = req['work']
            driver = req['driver']
            truck = req['truck']
            customers = req['customers']
            remarks = req['remarks']

            expense_report = Expense.objects.filter(pk__in=pk_list)

            if work:
                condition = Q(work_order__work_normal__work_id=work) | Q(work_order__work_agent_transport__work_id=work)
                filtered_report = Expense.objects.filter(condition)
            else:
                if customers:
                    condition1 = ~Q(work_order__detail__has_key='customer_name') & (Q(work_order__work_normal__principal__name__in=customers) | Q(work_order__work_agent_transport__principal__name__in=customers))
                    condition2 = Q(work_order__detail__has_key='customer_name') & Q(work_order__detail__customer_name__in=customers)
      
                    expense_report = expense_report.filter(condition1 | condition2)

                filter_dict = {}

                if "(empty)" in remarks:
                    expense_report = expense_report.filter(~Q(work_order__detail__has_key='remark') | Q(work_order__detail__remark__in=remarks))
                else:
                    set_if_not_none(filter_dict, 'work_order__detail__remark__in', remarks)
           
                set_if_not_none(filter_dict, 'work_order__driver__pk', driver)
                set_if_not_none(filter_dict, 'work_order__truck__pk', truck)

                filtered_report = expense_report.filter(**filter_dict)

            date_list = get_values_list(filtered_report, 'work_order__clear_date')

            filtered_report = order_expense_report(filtered_report)
            serializer = ExpenseThcSerializer(filtered_report, many=True)

            total_price_list = get_total_price_list(filtered_report)
            total_expense_list = get_total_expense_list(filtered_report)
            data = {
                'report_list': serializer.data,
                # 'date_list': date_list,

                'total_price_list': total_price_list,
                # 'total_expense_list': total_expense_list,
            }

            if page == 'expense':
                data['date_list'] = date_list
                data['total_expense_list'] = total_expense_list

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


# Total Expense
@csrf_exempt
def api_get_total_expense(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))

            year = int(req['year'])
            month = int(req['month'])
            period = int(req['period'])
            co = req['co']

            period_num, from_date, to_date = get_from_to_date(co, year, month, period)

            if from_date < to_date:
                # date_list = get_date_range(from_date, to_date)

                expense = Expense.objects.filter(Q(work_order__truck__owner=co) & Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lte=to_date))

                date_list = get_values_list(expense, 'work_order__clear_date')

                driver_list = get_driver_list(expense, co)

                total_report = []
                for driver in driver_list:
                    total_data = {}
                    total_data['truck'] = driver['truck']
                    total_data['driver'] = driver['employee']['full_name']

                    driver_expense = expense.filter(work_order__driver__pk=driver['id'])

                    daily_total_list = []
                    
                    for date in date_list:
                        daily_expense = driver_expense.filter(work_order__clear_date=date)
                        daily_total = daily_expense.aggregate(total=Sum('co_total') + Sum('cus_total'))['total'] or 0

                        daily_total_list.append(daily_total)

                    total_data['total'] = daily_total_list
                    total_report.append(total_data)

                thc_total_list = []
                date_total_list = []
                all_total_list = []

                try:
                    thc_add = Variable.objects.get(key='thc_add').value
                    thc_add = int(thc_add)
                except Variable.DoesNotExist:
                    thc_add = 0

                for date in date_list:
                    date_expense = expense.filter(work_order__clear_date=date)
                    date_total = date_expense.aggregate(total=Sum('co_total') + Sum('cus_total'))['total'] or 0

                    thc_count = date_expense.filter(co_expense__has_key='co_thc').count()
                    thc_total = thc_count * thc_add

                    thc_total_list.append(thc_total)
                    date_total_list.append(date_total)

                    all_total_list.append(date_total + thc_total)

                data = {
                    'from_date': from_date,
                    'to_date': to_date,

                    'period': period_num,

                    'total_report': total_report,
                    'date': date_list,

                    'thc_total_list': thc_total_list,
                    'date_total_list': date_total_list,
                    'all_total_list': all_total_list
                }
            
            else:
                driver_list = get_driver_list([], co)

                total_report = []
                for driver in driver_list:
                    total_data = {
                        'truck': driver['truck'],
                        'driver': driver['employee']['full_name'],
                        'total': []
                    }
                    total_report.append(total_data)

                data = {
                    'from_date': None,
                    'to_date': None,

                    'period': 0,

                    'total_report': total_report,
                    'date': [],

                    'thc_total_list': [],
                    'date_total_list': [],
                    'all_total_list': []
                }
                
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


def get_driver_list(report, co):
    if co == 'ndd':
        order = 'employee__co'
    else:
        order = '-employee__co'
    
    if report:
        driver_report_pk = report.values_list('work_order__driver__pk')
    else:
        driver_report_pk = []

    driver = Driver.objects.filter((Q(employee__co=co) & Q(employee__status='a')) | Q(pk__in=driver_report_pk)).order_by(order, 'truck__number', 'employee__first_name', 'employee__last_name')
    serializer = DriverSerializer(driver, many=True)

    return serializer.data

# Methods
def order_expense_report(report):
    return report.order_by('work_order__clear_date', 'work_order__driver__truck__number', 'work_order__driver__employee__first_name', \
                    'work_order__driver__employee__last_name', 'work_order__work_date', 'pk')


def get_from_to_date(co, year, month, period):
    if co == 'ndd':
        period_num = 3
    else:
        period_num = 2

    summary_date_list = ExpenseSummaryDate.objects.filter(co=co).order_by('-date')
    selected_month = summary_date_list.filter(Q(year__year_label=year) & Q(month=month))

    if period == 0:
        from_date = get_last_month_date(summary_date_list, month, year)
        if selected_month:
            to_date = selected_month.first().date

            if len(selected_month) < period_num:
                to_date = check_next_date(summary_date_list, to_date)
        else:
            to_date = check_next_date(summary_date_list, from_date)
    else:
        to_date = selected_month.order_by('date')[period-1].date

        if period == 1:
            from_date = get_last_month_date(summary_date_list, month, year)
        else:
            from_date = summary_date_list.filter(date__lt=to_date).first().date
    
    to_date = to_date - timedelta(days=1)

    period_count = selected_month.order_by('date').values_list('date', flat=True).distinct().count()
    
    return period_count, from_date, to_date

def get_last_month_date(date_list, month, year):
    if month == 1:
        last_month = date_list.filter(Q(year__year_label=year-1) & Q(month=12))
    else:
        last_month = date_list.filter(Q(year__year_label=year) & Q(month=month-1))

    if last_month:
        return last_month.first().date
    else:
        return datetime(year, month, 1).date()

def check_next_date(date_list, date):
    next_month = date + timedelta(days=30)
    today = datetime.now().date()
    next_date = date_list.filter(Q(date__gt=date) & Q(date__lte=next_month))
    if next_date:
        return next_date.last().date
    elif today < next_month:
        return today
    else:
        return next_month


def get_total_price_list(report_list):
    price_key = ['work_order__price__work', 'work_order__price__allowance', 'work_order__price__overnight']
    total_price_list = sum_from_key_list(report_list, price_key)
    return total_price_list

def get_total_expense_list(report_list):
    co_expense_key = ['co_expense__co_toll', 'co_expense__co_gate', 'co_expense__co_tire', 'co_expense__co_fine', 'co_expense__co_thc', 'co_expense__co_service', 'co_expense__co_other']
    cus_expense_key = ['cus_expense__cus_return', 'cus_expense__cus_gate', 'cus_expense__cus_other']

    co_expense_list = sum_from_key_list(report_list, co_expense_key)
    
    try:
        thc = Variable.objects.get(key='thc').value
        thc = int(thc)
    except Variable.DoesNotExist:
        thc = 0
    co_thc_count = report_list.filter(co_expense__has_key='co_thc').count()
    co_expense_list[4] = co_thc_count * thc

    co_total = sum(co_expense_list)
    co_expense_list.append(co_total)

    cus_expense_list = sum_from_key_list(report_list, cus_expense_key)
    cus_total = sum(cus_expense_list)
    cus_expense_list.append(cus_total)

    total_expense_list = co_expense_list + cus_expense_list
    total_expense_list.append(co_total + cus_total)

    return total_expense_list

def sum_from_key_list(report_list, key_list):
    total_list = []
    for key in key_list:
        price_list = report_list.values_list(key, flat=True)
        price_list = list(filter(None, price_list))
        sum_of_price = eval("+".join(price_list) + '+ 0')
        total_list.append(sum_of_price)

    return total_list


def get_customer_options_filter(report):
    detail_customer_options = get_values_list(report, 'work_order__detail__customer_name')

    customer = report.filter(~Q(work_order__detail__has_key='customer_name'))
    normal_customer_options = get_values_list(customer, 'work_order__work_normal__principal__name')
    agent_customer_options = get_values_list(customer, 'work_order__work_agent_transport__principal__name')

    customer_options = sorted(detail_customer_options + normal_customer_options + agent_customer_options)

    return customer_options

def get_values_list(expense_list, col):
    query_set = expense_list.order_by(col).values_list(col, flat=True).distinct()

    return list(filter(None, query_set))
