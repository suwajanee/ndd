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


@csrf_exempt
def api_get_daily_expense(request):
    if request.user.is_authenticated:
        # if request.method == "GET":
        #     date = datetime.today()
        #     co = 'ndd'
        if request.method == "POST":  
            req = json.loads(request.body.decode('utf-8'))
            date = req['date']
            co = req['co']
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except:
                return JsonResponse(False, safe=False)
        # else:
        #     return JsonResponse('Error', safe=False)

            work_expense = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__truck__owner=co)).order_by('work_order__driver__truck__number', 'work_order__driver__employee__first_name', 'work_order__work_date', 'pk')
            serializer = ExpenseSerializer(work_expense, many=True)

            driver_list = get_driver_list(work_expense, co)
            data = {
                'date': date.date(),
                'work_expense': serializer.data,
                'driver_list': driver_list
            }

            return JsonResponse(data, safe=False)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_daily_driver_expense(request):
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

            work_expense = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__driver__employee=driver)).order_by('work_order__work_date', 'pk')

            co_work_expense = work_expense.filter(work_order__truck__owner=co)
            not_co_work_expense = work_expense.filter(~Q(work_order__truck__owner=co))

            co_work = ExpenseSerializer(co_work_expense, many=True)
            not_co_work = ExpenseSerializer(not_co_work_expense, many=True)

            data = {
                "driver": driver_serializer.data,
                "truck": truck_data,
                "report": [co_work.data, not_co_work.data]
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


@csrf_exempt
def api_get_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            year = int(req['year'])
            month = int(req['month'])
            period = int(req['period'])
            co = req['co']

            selected_month, from_date, to_date = get_start_and_end_date(co, year, month, period)

            expense = Expense.objects.filter(work_order__truck__owner=co)

            if to_date:
                expense = expense.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lt=to_date))
            else:
                expense = expense.filter(work_order__clear_date__gte=from_date)

            expense = order_expense_report(expense)

            pk_list = expense.values_list('pk', flat=True).distinct()

            expense_serializer = ExpenseThcSerializer(expense, many=True)
            period_serializer = ExpenseSummaryDateSerializer(selected_month, many=True)

            customer_list, remark_list = get_filter_choices(expense)
            total_list = get_total_list(expense)            

            data = {
                'period': period_serializer.data,
                'expense': expense_serializer.data,
                'pk_list': list(pk_list),

                'customer_list': customer_list,
                'remark_list': ['(empty)'] + remark_list,

                'total': total_list
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_filter_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            
            pk_list = req['pk_list']
            work = req['work']
            driver = req['driver']
            truck = req['truck']
            customers = req['customers']
            remarks = req['remarks']

            expense_report = Expense.objects.filter(pk__in=pk_list)
            customer_list, remark_list = get_filter_choices(expense_report)

            if work:
                condition = Q(work_order__work_normal__work_id=work) | Q(work_order__work_agent_transport__work_id=work)
                filtered_report = Expense.objects.filter(condition)
            else:
                if customers:
                    condition = Q(work_order__work_normal__principal__name__in=customers) | Q(work_order__work_agent_transport__principal__name__in=customers) | \
                                Q(work_order__detail__customer_name__in=customers)
                    
                    expense_report = expense_report.filter(condition)

                filter_dict = {}

                if "(empty)" in remarks:
                    expense_report = expense_report.filter(~Q(work_order__detail__has_key='remark') | Q(work_order__detail__remark__in=remarks))
                else:
                    set_if_not_none(filter_dict, 'work_order__detail__remark__in', remarks)
           
                set_if_not_none(filter_dict, 'work_order__driver__pk', driver)
                set_if_not_none(filter_dict, 'work_order__truck__pk', truck)

                filtered_report = expense_report.filter(**filter_dict)

            filtered_report = order_expense_report(filtered_report)
            serializer = ExpenseThcSerializer(filtered_report, many=True)

            total_list = get_total_list(filtered_report)
            data = {
                'expense': serializer.data,
                'total': total_list,

                'customer_list': customer_list,
                'remark_list': ['(empty)'] + remark_list,
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


# Hereeeeeee
@csrf_exempt
def api_get_summary_expense(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))

            year = int(req['year'])
            month = int(req['month'])
            period = int(req['period'])
            co = req['co']

            selected_month, from_date, to_date = get_start_and_end_date(co, year, month, period)

            date_list = get_date_range(from_date, to_date)

            expense = Expense.objects.filter(Q(work_order__truck__owner=co) & Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lt=to_date))

            driver_list = get_driver_list(expense, co)

            total_expense_list = []
            for driver in driver_list:
                summary_data = {}
                summary_data['driver'] = driver['employee']['detail']['full_name']
                driver_expense = expense.filter(work_order__driver__pk=driver['id'])

                summary_list = []
                for date in date_list:
                    total_expense = 0

                    date_expense = driver_expense.filter(work_order__clear_date=date)
                    total_expense = date_expense.annotate(company=Cast(KeyTextTransform('company', 'total_expense'), FloatField()), \
                                customer=Cast(KeyTextTransform('customer', 'total_expense'), FloatField())).aggregate(total=Sum('company') + Sum('customer'))['total'] or 0

                    summary_list.append(total_expense)
                summary_data['total'] = summary_list

                total_expense_list.append(summary_data)

            thc_count_list = []
            for date in date_list:
                thc = expense.filter(work_order__clear_date=date, co_expense__has_key='co_thc').count()
                thc_count_list.append(thc*110)

            data = {
                'total': total_expense_list,
                'date': date_list,
                'thc': thc_count_list
            }
                
            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


def get_date_range(from_date, to_date):
    date_list = []
    while from_date < to_date:
        date_list.append(from_date)
        from_date = from_date + timedelta(days=1)
    return date_list


def get_driver_list(report, co):
    if co == 'ndd':
        order = 'employee__co'
    else:
        order = '-employee__co'

    driver_report_pk = report.values_list('work_order__driver__pk')

    driver = Driver.objects.filter((Q(employee__co=co) & Q(employee__status='a')) | Q(pk__in=driver_report_pk)).order_by(order, 'truck__number', 'employee__first_name', 'employee__last_name')
    serializer = DriverSerializer(driver, many=True)

    return serializer.data

# Methods
def order_expense_report(report):
    return report.order_by('work_order__clear_date', 'work_order__driver__truck__number', 'work_order__driver__employee__first_name', \
                    'work_order__driver__employee__last_name', 'work_order__work_date', 'pk')


def get_start_and_end_date(co, year, month, period):
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
    
    return selected_month, from_date, to_date

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
    next_date = date_list.filter(date__gt=date)
    if next_date:
        return next_date.last().date
    else:
        return datetime.now().date()


def get_total_list(report_list):
    price_key = ['work_order__price__work', 'work_order__price__allowance', 'work_order__price__overnight']
    co_expense_key = ['co_expense__co_toll', 'co_expense__co_gate', 'co_expense__co_tire', 'co_expense__co_fine', 'co_expense__co_thc', 'co_expense__co_service', 'co_expense__co_other']
    cus_expense_key = ['cus_expense__cus_return', 'cus_expense__cus_gate', 'cus_expense__cus_other']

    total_price_list = sum_expense_list(report_list, price_key)
    
    co_expense_list = sum_expense_list(report_list, co_expense_key)
    
    co_thc_count = report_list.filter(co_expense__has_key='co_thc').count()
    co_expense_list[4] = co_thc_count * 150

    co_total = sum(co_expense_list)
    co_expense_list.append(co_total)

    cus_expense_list = sum_expense_list(report_list, cus_expense_key)
    cus_total = sum(cus_expense_list)
    cus_expense_list.append(cus_total)

    total_expense_list = co_expense_list + cus_expense_list
    total_expense_list.append(co_total + cus_total)

    return [total_price_list, total_expense_list]

def sum_expense_list(report_list, key_list):
    total_list = []
    for key in key_list:
        price_list = report_list.values_list(key, flat=True)
        price_list = list(filter(None, price_list))
        sum_of_price = eval("+".join(price_list) + '+ 0')
        total_list.append(sum_of_price)

    return total_list


def get_filter_choices(report):
    remark_choices = get_values_list(report, 'work_order__detail__remark')

    detail_customer_choices = get_values_list(report, 'work_order__detail__customer_name')

    customer = report.filter(~Q(work_order__detail__has_key='customer_name'))
    normal_customer_choices = get_values_list(customer, 'work_order__work_normal__principal__name')
    agent_customer_choices = get_values_list(customer, 'work_order__work_agent_transport__principal__name')

    customer_choices = sorted(detail_customer_choices + normal_customer_choices + agent_customer_choices)

    return customer_choices, remark_choices

def get_values_list(expense_list, col):
    query_set = expense_list.order_by(col).values_list(col, flat=True).distinct()

    return list(filter(None, query_set))
