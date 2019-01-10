# -*- coding: utf-8 -*-

import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import CustomerCustom,FormDetail
from ..serializers import CustomerSettingSerializer
from customer.models import Principal


@csrf_exempt
def api_get_customer_custom(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            customer_id = req['customer']

            customer_setting = CustomerCustom.objects.filter(customer__pk=customer_id)
            serializer = CustomerSettingSerializer(customer_setting, many=True)
            return JsonResponse(serializer.data, safe=False)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_customer_custom(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            customer = req['customer_setting']
            form = customer['form']

            data = {
                'customer': Principal.objects.get(pk=customer['customer']['id']),
                'sub_customer': re.sub(' +', ' ', customer['sub_customer'].strip()),
                'customer_title': re.sub(' +', ' ', customer['customer_title'].strip()),
            }

            if form:
                data['form'] = FormDetail.objects.get(pk=customer['form']['id'])

            customer_setting = CustomerCustom(**data)
            customer_setting.save()

            return api_get_customer_custom(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_customer_custom(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            customer = req['customer_setting']
            sub_customer = customer['sub_customer']
            customer_title = customer['customer_title']
            form = customer['form']

            customer_setting = CustomerCustom.objects.get(pk=customer['id'])

            if sub_customer:
                customer_setting.sub_customer = re.sub(' +', ' ', customer['sub_customer'].strip())
            else:
                customer_setting.sub_customer = ''
            
            if customer_title:
                customer_setting.customer_title = re.sub(' +', ' ', customer['customer_title'].strip())
            else:
                customer_setting.customer_title = ''

            if form:
                customer_setting.form = FormDetail.objects.get(pk=form['id'])
            else:
                customer_setting.form = None

            customer_setting.save()

            return api_get_customer_custom(request)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_delete_customer_custom(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            setting_id = req["setting_id"]

            customer_setting = CustomerCustom.objects.get(pk=setting_id)
            customer_setting.delete()

            return api_get_customer_custom(request)
    return JsonResponse('Error', safe=False)  