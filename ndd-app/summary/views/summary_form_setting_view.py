# -*- coding: utf-8 -*-

import copy
import json
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import Avg, Count, Min, Sum
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import Year, FormDetail, CustomerForm, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from ..serializers import FormDetailSerializer


@csrf_exempt
def api_get_summary_form(request):
    if request.user.is_authenticated:
        forms = FormDetail.objects.all().order_by('pk')
        serializer = FormDetailSerializer(forms, many=True)
        return JsonResponse(serializer.data, safe=False)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_add_summary_form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            data = req['form']

            data['form_name'] = re.sub(' +', ' ', data['form_name'].strip())
            form_setting = FormDetail(**data)
            form_setting.save()

            return api_get_summary_form(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_edit_summary_form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            form_id = req['form_id']
            data = req['form']

            form = FormDetail.objects.get(pk=form_id)
            form.form_name = re.sub(' +', ' ', data['form_name'].strip())
            form.form_detail = data['form_detail']
            form.save()

            return api_get_summary_form(request)

    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_delete_summary_form(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            form_id = req["form_id"]

            form = FormDetail.objects.get(pk=form_id)
            form.delete()

            return api_get_summary_form(request)
    return JsonResponse('Error', safe=False)  