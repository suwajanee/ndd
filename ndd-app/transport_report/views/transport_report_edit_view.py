# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import WorkOrder
from ..models import Expense
from ..models import ExpenseSummaryDate
from ..models import Variable
from agent_transport.models import AgentTransport
from booking.models import Booking
from employee.models import Driver
from truck.models import Truck


@csrf_exempt
def api_edit_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            work_type = req['work_type']
            work_id = req['work_id']

            order_data = req['work_order']
            detail = req['detail']
            price = req['price']

            co_expense = req['co_expense']
            cus_expense = req['cus_expense']
            total_expense = req['total_expense']

            work_order = WorkOrder.objects.get(pk=order_data['pk'])
            if work_type == 'normal':
                work_order.work_normal = Booking.objects.get(work_id=work_id)
                work_order.work_agent_transport = None
            else:
                work_order.work_normal = None
                work_order.work_agent_transport = AgentTransport.objects.get(work_id=work_id)

            work_order.driver = Driver.objects.get(employee__pk=order_data['driver'])
            work_order.truck = Truck.objects.get(pk=order_data['truck'])

            work_order.work_date = order_data['work_date']
            work_order.order_type = order_data['order_type']
            work_order.double_container = order_data['double_container']
            work_order.detail = detail
            work_order.price = price
            work_order.save()

            expense = Expense.objects.get(pk=order_data['expense_pk'])

            try:
                thc_rate = int(Variable.objects.get(key='thc').value)
            except Variable.DoesNotExist:
                thc_rate = 0

            if 'thc_rate' in co_expense:
                co_expense.pop('thc_rate')
                total_expense['company'] -= thc_rate
            expense.co_expense = co_expense
            expense.cus_expense = cus_expense
            expense.total_expense = total_expense
            expense.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)
