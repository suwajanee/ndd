# -*- coding: utf-8 -*-

import copy
import json
import re

from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from customer.models import Principal
from ..serializers import SummaryWeekSerializer


@csrf_exempt
def api_edit_summary_customer_detail(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            details = req['customer_detail']

            for detail in details:
                date_billing = detail['date_billing']
                date_end = detail['date_end']

                summary_customer = SummaryCustomer.objects.get(pk=detail['id'])

                if not date_billing:
                    date_billing = None
                if not date_end:
                    date_end = None
                
                summary_customer.date_billing = date_billing
                summary_customer.date_end = date_end
                summary_customer.detail = detail['detail']
                summary_customer.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)