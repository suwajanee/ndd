# -*- coding: utf-8 -*-

import json
import re

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import FormDetail
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