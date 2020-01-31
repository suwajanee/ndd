# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import WorkOrder
from ..models import Expense
from ..models import ExpenseSummaryDate


@csrf_exempt
def api_delete_expense_report(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            report_pk = req['id']

            work_order = WorkOrder.objects.get(pk=report_pk)

            expense = Expense.objects.filter(work_order=work_order).delete()
            work_order.delete()

            return JsonResponse('Success', safe=False)
    return JsonResponse('Error', safe=False)
