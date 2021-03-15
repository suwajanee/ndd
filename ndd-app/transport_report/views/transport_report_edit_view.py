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
            co_total = req['co_total']
            cus_total = req['cus_total']

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

            expense.co_expense = co_expense
            expense.cus_expense = cus_expense
            expense.co_total = co_total
            expense.cus_total = cus_total

            expense.save()

            serializer = WorkOrderSerializer(work_order, many=False)

            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_price_list(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            work_order_id_list = req['work_id_list']
            work_order_data_list = req['work_data_list']

            work_order_list = WorkOrder.objects.filter(pk__in=work_order_id_list)

            saved_list = []
            for data in work_order_data_list:
                work = work_order_list.get(pk=data['id'])
                work.price = data['price']
                work.detail = data['detail']
                work.save()

                serializer = WorkOrderSerializer(work, many=False)
                saved_list.append(serializer.data)

            return JsonResponse(saved_list, safe=False)
    return JsonResponse('Error', safe=False)
