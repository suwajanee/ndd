# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import AgentTransport
from ..serializers import AgentTransportSerializer
from summary.views.summary_week_view import get_week_details


@csrf_exempt
def api_get_work_list(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            week = req['week']
            year = req['year']
            customer = req['customer']

            week, week_serializer = get_week_details(week, year)

            agent_transports = AgentTransport.objects.filter(Q(principal__pk=customer) & Q(date__lte=week.date_end) & ~Q(status=0)).order_by('date', 'shipper__name', 'work_type', 'booking_no', 'work_id')

            serializer = AgentTransportSerializer(agent_transports, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)  
    
