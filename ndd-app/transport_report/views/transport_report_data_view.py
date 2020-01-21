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
            date = datetime.strptime(date, '%Y-%m-%d')

        else:
            return JsonResponse('Error', safe=False)

        work_expense = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__truck__owner=co)).order_by('work_order__driver__truck__number', 'work_order__driver__employee__first_name', 'work_order__work_date')
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

            driver = Employee.objects.get(pk=driver_id)
            driver_serializer = EmployeeSerializer(driver, many=False)

            try:
                truck = Driver.objects.get(employee=driver).truck
                truck_serializer = TruckSerializer(truck, many=False)
                truck_data = truck_serializer.data

            except:
                truck_data = {}

            work_expense = Expense.objects.filter(Q(work_order__clear_date=date) & Q(work_order__driver__employee=driver)).order_by('work_order__work_date')
            work_serializer = ExpenseSerializer(work_expense, many=True)

            data = {
                "driver": driver_serializer.data,
                "truck": truck_data,
                "report": work_serializer.data
            }

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)


@csrf_exempt
def api_get_by_summary_date(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            summary_date_id = req['summary_date_id']

            all_summary_date = ExpenseSummaryDate.objects.all()

            to_before_date = all_summary_date.get(pk=summary_date_id)
            from_date = all_summary_date.filter(date__lt=date.selected.date).order_by('-date').first()

            work_expense = Expense.objects.filter(Q(work_order__clear_date__gte=from_date) & Q(work_order__clear_date__lt=to_before_date)) \
                .order_by('work_order__driver__truck__number', 'work_order__driver__employee_first_name', 'work_order__work_date')

            serializer = ExpenseSerializer(work_expense, many=True)

            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)



