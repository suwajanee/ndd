# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import WorkOrder
from ..models import Expense
from ..models import ExpenseSummaryDate
from ..serializers import WorkOrderSerializer
from ..serializers import ExpenseSerializer
from ..serializers import ExpenseSummaryDateSerializer
from ..serializers import TruckSerializer
from booking.views.utility.functions import set_if_not_none
from employee.models import Driver
from employee.models import Employee
from employee.serializers import EmployeeSerializer


@csrf_exempt
def api_get_daily_expense(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            date = datetime.today()
            co = 'ndd'

        elif request.method == "POST":  
            req = json.loads(request.body.decode('utf-8'))
            date = req['date']
            co = req['co']
            try:
                date = datetime.strptime(date, '%Y-%m-%d')
            except:
                return JsonResponse(False, safe=False)

        else:
            return JsonResponse('Error', safe=False)

        work_expense = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__truck__owner=co)).order_by('work_order__driver__truck__number', 'work_order__driver__employee__first_name', 'work_order__work_date', 'pk')
        serializer = ExpenseSerializer(work_expense, many=True)

        data = {
            'date': date.date(),
            'work_expense': serializer.data
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


            expense = Expense.objects.filter(work_order__truck__owner=co)

            if to_date:
                expense = expense.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lt=to_date))
            else:
                expense = expense.filter(work_order__clear_date__gte=from_date)
            

            expense = expense.order_by('work_order__clear_date', 'work_order__driver__truck__number', 'work_order__driver__employee__first_name', \
                    'work_order__driver__employee__last_name', 'work_order__work_date', 'pk')

            pk_list = expense.values_list('pk', flat=True).distinct()
            remark_list = get_values_list(expense, 'work_order__detail__remark')
            work_normal_list = get_values_list(expense, 'work_order__work_normal__work_id')
            work_agent_list = get_values_list(expense, 'work_order__work_agent_transport__work_id')

            detail_customer_list = get_values_list(expense, 'work_order__detail__customer_name')

            customer = expense.filter(~Q(work_order__detail__has_key='customer_name'))
            normal_customer_list = get_values_list(customer, 'work_order__work_normal__principal__name')
            agent_customer_list = get_values_list(customer, 'work_order__work_agent_transport__principal__name')

            work_list = sorted(work_normal_list + work_agent_list)
            customer_list = sorted(detail_customer_list + normal_customer_list + agent_customer_list)

            expense_serializer = ExpenseSerializer(expense, many=True)

            period_serializer = ExpenseSummaryDateSerializer(selected_month, many=True)

            data = {
                'period': period_serializer.data,
                'expense': expense_serializer.data,
                'pk_list': list(pk_list),
                'work_list': work_list,
                'remark_list': remark_list,
                'customer_list': customer_list
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

def get_values_list(expense_list, col):
    query_set = expense_list.order_by(col).values_list(col, flat=True).distinct()

    return list(filter(None, query_set))

def get_last_month_date(date_list, month, year):
    if month == 1:
        last_month = date_list.filter(Q(year__year_label=year-1) & Q(month=12))
    else:
        last_month = date_list.filter(Q(year__year_label=year) & Q(month=month-1))

    if last_month:
        return last_month.first().date
    else:
        return datetime(year, month, 1)

def check_next_date(date_list, date):
    next_date = date_list.filter(date__gt=date)
    if next_date:
        return next_date.last().date
    else:
        return datetime.now()