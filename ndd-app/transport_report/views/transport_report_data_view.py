# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import json

from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.core.paginator import Paginator
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
from ..serializers import ExpenseContainerSerializer
from ..serializers import ExpenseSummaryDateSerializer
from ..serializers import TruckSerializer
from booking.views.utility.functions import set_if_not_none
from employee.models import Driver
from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.serializers import DriverSerializer
from truck.models import Truck
from truck.serializers import TruckSerializer


# Get Order Type by Work ID
@csrf_exempt
def api_get_used_order_type_by_work_id(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            work_id = req['work_id']
            try:
                order_type_list = WorkOrder.objects.filter(Q(work_normal__work_id=work_id) | Q(work_agent_transport__work_id=work_id)).values_list('order_type', flat=True)
                order_type_list = list(order_type_list)
            except:
                order_type_list = []

            return JsonResponse(order_type_list, safe=False)
    return JsonResponse('Error', safe=False)


# Daily Expense & Daily Driver Expense
@csrf_exempt
def api_get_default_driver_truck(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            driver_id = req['driver_id']
            try:
                driver = Employee.objects.get(pk=driver_id)
                driver_serializer = EmployeeSerializer(driver, many=False)
            except:
                return JsonResponse(False, safe=False)
            
            try:
                truck = Driver.objects.get(employee=driver).truck
                truck_serializer = TruckSerializer(truck, many=False)
                truck_data = truck_serializer.data
            except:
                truck_data = {}
            
            data = {
                'driver': driver_serializer.data,
                'truck': truck_data
            }
            return JsonResponse(data, safe=False)
    return JsonResponse(False, safe=False)

@csrf_exempt
def api_get_daily_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            date = req['date']
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except:
                return JsonResponse(False, safe=False)
            
            report = Expense.objects.filter(work_order__clear_date=date)
            report = order_expense_report(report)

            driver_list = get_driver_list(report)
            truck_list = get_truck_list(report)

            if 'driver' in req:
                driver_id = req['driver']
                report = report.filter(work_order__driver__employee__pk=driver_id)

            expense_serializer = ExpenseSerializer(report, many=True)
            total = report.order_by('work_order__clear_date').aggregate(total=Sum('co_total') + Sum('cus_total'))['total']

            data = {
                'driver_list': driver_list,
                'truck_list': truck_list,
                'expense_list': expense_serializer.data,
                'total': total
            }

            return JsonResponse(data, safe=False)
    return JsonResponse(False, safe=False)

# Expense page & Filter
@csrf_exempt
def api_get_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            page_num = req['page_num']
            page_name = req['page_name']
            year = int(req['year'])
            month = int(req['month'])
            period = int(req['period'])

            period_num, from_date, to_date = get_from_to_date(year, month, period)

            if from_date <= to_date:
                expense = Expense.objects.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lte=to_date))
                expense = order_expense_report(expense)
                
                pk_list = expense.values_list('pk', flat=True).distinct()

                remark_list = get_values_list(expense, 'work_order__detail__remark')
                customer_list = get_customer_options_filter(expense)

                total_price_list = get_total_price_list(expense)
                total_expense_list = get_total_expense_list(expense)

                driver_list = get_driver_list(expense)
                truck_list = get_truck_list(expense)

                report_page, page_range = paginate_report(expense, page_num)

                data = {
                    'from_date': from_date,
                    'to_date': to_date,

                    'page_range': page_range,
                    'page_num': report_page.number,

                    'period': period_num,

                    'pk_list': list(pk_list),

                    'driver_list': driver_list,
                    'truck_list': truck_list,

                    'customer_list': customer_list,
                    'remark_list': ['(empty)'] + remark_list,

                    'total_price_list': total_price_list,
                }

                if page_name == 'expense':
                    serializer = ExpenseThcSerializer(report_page, many=True)
                    data['report_list'] = serializer.data
                    data['total_expense_list'] = total_expense_list
                else:
                    serializer = ExpenseContainerSerializer(report_page, many=True)
                    data['report_list'] = serializer.data

            else:
                driver_list = get_driver_list([])
                truck_list = get_truck_list([])

                data = {
                    'from_date': None,
                    'to_date': None,

                    'page_range': [],
                    'page_num': 0,

                    'period': 0,
                    'report_list': [],
                    'pk_list': [],

                    'driver_list': driver_list,
                    'truck_list': truck_list,

                    'customer_list': [],
                    'remark_list': [],

                    'total_price_list': [],
                    'total_expense_list': [],
                }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

def paginate_report(report, page_num):
    try:
        row_limit = Variable.objects.get(key='row_limit').value
    except:
        row_limit = 150
    paginator = Paginator(report, row_limit)
    try:
        report_page = paginator.page(page_num)
    except:
        report_page = paginator.page(paginator.num_pages)
    
    return report_page, list(paginator.page_range)

@csrf_exempt
def api_get_expense_report_by_id_list(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))

            page_name = req['page_name']
            page_num = req['page_num']
            pk_list = req['pk_list']

            expense_report = Expense.objects.filter(pk__in=pk_list)
            expense_report = order_expense_report(expense_report)

            total_price_list = get_total_price_list(expense_report)
            total_expense_list = get_total_expense_list(expense_report)

            report_page, page_range = paginate_report(expense_report, page_num)

            if page_name == 'expense':
                serializer = ExpenseThcSerializer(report_page, many=True)
                data = {
                    'report_list': serializer.data,
                    'total_price_list': total_price_list,
                    'total_expense_list': total_expense_list,

                    'page_range': page_range,
                    'page_num': report_page.number
                }
            else:
                serializer = ExpenseContainerSerializer(report_page, many=True)
                data = {
                    'report_list': serializer.data,
                    'total_price_list': total_price_list,

                    'page_range': page_range,
                    'page_num': report_page.number
                }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


@csrf_exempt
def api_filter_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            
            page_name = req['page_name']
            page_num = req['page_num']
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

            filtered_report = order_expense_report(filtered_report)
            filtered_pk_list = filtered_report.values_list('pk', flat=True).distinct()

            total_price_list = get_total_price_list(filtered_report)
            total_expense_list = get_total_expense_list(filtered_report)

            report_page, page_range = paginate_report(filtered_report, page_num)

            if page_name == 'expense':
                serializer = ExpenseThcSerializer(report_page, many=True)
                data = {
                    'report_list': serializer.data,
                    'total_price_list': total_price_list,

                    'total_expense_list': total_expense_list,
                    'pk_list': list(filtered_pk_list),

                    'page_range': page_range,
                    'page_num': report_page.number
                }
            else:
                serializer = ExpenseContainerSerializer(report_page, many=True)
                data = {
                    'report_list': serializer.data,
                    'total_price_list': total_price_list,
                    'pk_list': list(filtered_pk_list),

                    'page_range': page_range,
                    'page_num': report_page.number
                }

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

            period_num, from_date, to_date = get_from_to_date(year, month, period)

            if from_date <= to_date:
                expense = Expense.objects.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lte=to_date))

                date_list = get_values_list(expense, 'work_order__clear_date')

                driver_list = get_driver_list(expense)

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
                driver_list = get_driver_list([])

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

# Total Truck
@csrf_exempt
def api_get_total_truck(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))

            year = int(req['year'])
            month = int(req['month'])

            period_num, from_date, to_date = get_from_to_date(year, month, 0)

            if from_date <= to_date:
                expense = Expense.objects.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lte=to_date))

                truck_list = get_truck_list(expense)
                try:
                    thc = Variable.objects.get(key='thc').value
                    thc = int(thc)
                except Variable.DoesNotExist:
                    thc = 0

                price_list = []
                allowance_list = []
                co_expense_list = []
                for truck in truck_list:
                    truck_expense = expense.filter(work_order__truck__pk=truck['id'])

                    total_price = get_total_price_list(truck_expense)
                    price_list.append(total_price[0])
                    allowance_list.append(total_price[1] + total_price[2])

                    total_co_expense = truck_expense.aggregate(total_co_expense=Sum('co_total'))['total_co_expense'] or 0

                    if thc > 0:
                        total_thc = sum_from_key_list(truck_expense, ['co_expense__co_thc'])[0]
                        thc_count = truck_expense.filter(co_expense__has_key='co_thc').count()
                        total_co_expense += (thc_count * thc) - total_thc
                    
                    co_expense_list.append(float(total_co_expense))
                
                data = {
                    'from_date': from_date,
                    'to_date': to_date,

                    'truck': truck_list,
                    'price': price_list,
                    'allowance': allowance_list,
                    'co_expense': co_expense_list
                }
            
            else:
                truck_list = get_truck_list([])
                init_list = [0] * len(truck_list)

                data = {
                    'from_date': None,
                    'to_date': None,

                    'truck': truck_list,
                    'price': init_list,
                    'allowance': init_list,
                    'co_expense': init_list
                }

            return JsonResponse(data, safe=False)
    return JsonResponse(False, safe=False)


def get_driver_list(report):
    if report:
        driver_report_pk = report.values_list('work_order__driver__pk')
    else:
        driver_report_pk = []

    driver = Driver.objects.filter(Q(employee__status='a') | Q(pk__in=driver_report_pk)).order_by('truck__number', 'employee__first_name', 'employee__last_name')
    serializer = DriverSerializer(driver, many=True)

    return serializer.data

def get_truck_list(report):
    if report:
        truck_report_pk = report.values_list('work_order__truck__pk')
    else:
        truck_report_pk = []
    
    truck = Truck.objects.filter(~Q(status='s') | Q(pk__in=truck_report_pk)).order_by('number')
    serializer = TruckSerializer(truck, many=True)

    return serializer.data


# Methods
def order_expense_report(report):
    return report.order_by('work_order__clear_date', 'work_order__driver__truck__number', 'work_order__driver__employee__first_name', \
                    'work_order__driver__employee__last_name', 'work_order__work_date', 'pk')


def get_from_to_date(year, month, period):
    summary_date_list = ExpenseSummaryDate.objects.all().order_by('-date')
    selected_month = summary_date_list.filter(Q(year__year_label=year) & Q(month=month))
    if period == 0:
        from_date = get_last_month_date(summary_date_list, month, year)
        if selected_month:
            to_date = selected_month.first().date
            next_date = summary_date_list.filter(date__gt=to_date)
            if not next_date and len(selected_month) < 3:
                to_date = get_next_date(summary_date_list, to_date)
        else:
            to_date = get_next_date(summary_date_list, from_date)
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

def get_next_date(date_list, date):
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

    co_expense_list, co_total = total_co_expense(report_list)
    # co_total = sum(co_expense_list)
    co_expense_list.append(co_total)

    cus_expense_list, cus_total = total_cus_expense(report_list)
    # cus_total = sum(cus_expense_list)
    cus_expense_list.append(cus_total)

    total_expense_list = co_expense_list + cus_expense_list
    total_expense_list.append(co_total + cus_total)

    return total_expense_list

def total_co_expense(report_list):
    expense_key = ['co_expense__co_toll', 'co_expense__co_gate', 'co_expense__co_tire', 'co_expense__co_fine', 'co_expense__co_thc', 'co_expense__co_service', 'co_expense__co_other']
    expense_list = sum_from_key_list(report_list, expense_key)

    try:
        thc = Variable.objects.get(key='thc').value
        thc = int(thc)
    except Variable.DoesNotExist:
        thc = 0
    
    if thc > 0:
        co_thc_count = report_list.filter(co_expense__has_key='co_thc').count()
        expense_list[4] = co_thc_count * thc

    total = sum(expense_list)

    return expense_list, total

def total_cus_expense(report_list):
    expense_key = ['cus_expense__cus_return', 'cus_expense__cus_gate', 'cus_expense__cus_other']
    expense_list = sum_from_key_list(report_list, expense_key)
    total = sum(expense_list)
    return expense_list, total

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
