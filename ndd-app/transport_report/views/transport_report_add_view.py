# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import WorkOrder
from ..models import Expense
from ..models import ExpenseSummaryDate
from agent_transport.models import AgentTransport
from booking.models import Booking
from employee.models import Driver
from truck.models import Truck


@csrf_exempt
def api_add_expense_report(request):
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

            if work_type == 'normal':
                order_data['work_normal'] = Booking.objects.get(work_id=work_id)
            else:
                order_data['work_agent_transport'] = AgentTransport.objects.get(work_id=work_id)
            
            order_data['driver'] = Driver.objects.get(employee__pk=order_data['driver'])
            order_data['truck'] = Truck.objects.get(pk=order_data['truck'])
            order_data['detail'] = detail
            order_data['price'] = price

            work_order = WorkOrder(**order_data)
            work_order.save()

            expense_data = {
                'work_order': work_order,
                'co_expense': co_expense,
                'cus_expense': cus_expense,
                'total_expense': total_expense
            }

            expense = Expense(**expense_data)
            expense.save()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)
            
