# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import InvoiceDetail
from ..serializers import CommissionSerializer
from booking.views.utility.functions import set_if_not_none
from agent_transport.models import AgentTransport


@csrf_exempt
def api_get_commission_data(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            month = req['month']
            week = req['week']
            customer = req['customer']
            work = req['work']
            work_type = req['work_type']

            agent = AgentTransport.objects.filter(Q(principal__pk=customer))
            if work_type:
                agent = agent.filter(Q(work_type=work_type))

            if work == 'ndd':
                agent = agent.filter(~Q(pickup_tr__icontains='vts') & ~Q(return_tr__icontains='vts'))
            elif work == 'vts':
                agent = agent.filter(Q(pickup_tr__icontains='vts') | Q(return_tr__icontains='vts'))

            filter_dict = {}
            if week:
                set_if_not_none(filter_dict, 'invoice__customer_week__week__pk', week)
            else:
                set_if_not_none(filter_dict, 'invoice__customer_week__week__year__year_label', year)
                set_if_not_none(filter_dict, 'invoice__customer_week__week__month', month)

            filter_dict['work_agent_transport__in'] = agent

            commission = InvoiceDetail.objects.filter(Q(**filter_dict)).order_by('invoice__invoice_no', 'work_agent_transport__date', 'pk')
            serializer = CommissionSerializer(commission, many=True)

            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)