# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import CustomerCustom, Invoice, SummaryCustomer, SummaryWeek
from customer.models import Principal
from booking.views.utility.functions import check_key_detail


@csrf_exempt
def api_edit_summary_customer_detail(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            details = req['customer_detail']

            for detail in details:
                date_billing = detail['date_billing']
                date_due = detail['date_due']

                summary_customer = SummaryCustomer.objects.get(pk=detail['id'])

                if not date_billing:
                    date_billing = None
                if not date_due:
                    date_due = None
                if detail['remark'] and not summary_customer.detail:
                    summary_customer.detail = {}

                summary_customer.date_billing = date_billing
                summary_customer.date_due = date_due
                summary_customer.detail = check_key_detail(summary_customer.detail, detail, 'remark', True)
                summary_customer.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_summary_customer_status(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            customer_id = req['id']
            customer_status = req['status']

            summary_customer = SummaryCustomer.objects.get(pk=customer_id)

            summary_customer.status = customer_status
            summary_customer.save()

            return JsonResponse(True, safe=False)
    return JsonResponse('Error', safe=False)


# Method
def add_summary_customer(detail):
    data = {
        'week': SummaryWeek.objects.get(pk=detail['week']),
        'customer_main': Principal.objects.get(pk=detail['customer_main'])
    }
    if 'customer_custom' in detail:
        data['customer_custom'] = CustomerCustom.objects.get(pk=detail['customer_custom'])

    summary_customer = SummaryCustomer(**data)
    summary_customer.save()

    return summary_customer

def delete_summary_customer(summary_customer):
    invoice_count = Invoice.objects.filter(customer_week__pk=summary_customer).count()
    if invoice_count == 0:
        summary_customer = SummaryCustomer.objects.get(pk=summary_customer)
        summary_customer.delete()
    return True
