# -*- coding: utf-8 -*-

from datetime import datetime
import json
import re

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

            today = datetime.today()

            week, week_serializer = get_week_details(week, year)

            agent_transports = AgentTransport.objects.filter(Q(principal__pk=customer) & ~Q(status=0) & ((Q(date__lte=today) & Q(date__gte=week.date_start)) | \
                                (Q(date__lte=week.date_end) & ~Q(summary_status='1')))).order_by('date', 'shipper__name', 'work_type', 'operation_type', 'booking_no', 'work_id')

            serializer = AgentTransportSerializer(agent_transports, many=True)
            return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False)  
    
def agent_transport_summary_status(work_id, status):
    agent_transports = AgentTransport.objects.filter(pk__in=work_id).update(summary_status=status)
    return JsonResponse(True, safe=False)

def agent_transport_edit_summary(agent_transports):
    for agent_transport in agent_transports:
        agent_transport_save = AgentTransport.objects.get(pk=agent_transport['id'])

        agent_transport_save.booking_no = re.sub(' +', ' ', agent_transport['booking_no'].strip())
        agent_transport_save.pickup_from = re.sub(' +', ' ', agent_transport['pickup_from'].strip())
        agent_transport_save.return_to = re.sub(' +', ' ', agent_transport['return_to'].strip())

        if 'container_1' in agent_transport:
            agent_transport_save.container_1 = re.sub(' +', ' ', agent_transport['container_1'].strip())
        if 'container_2' in agent_transport:
            agent_transport_save.container_2 = re.sub(' +', ' ', agent_transport['container_2'].strip())
        agent_transport_save.size = re.sub(' +', ' ', agent_transport['size'].strip())
        agent_transport_save.agent = re.sub(' +', ' ', agent_transport['agent'].strip())
        agent_transport_save.save()

    return True

@csrf_exempt
def api_get_agent_transport_daily_works(request):
    if request.user.is_authenticated:
        if request.method == "GET": 
            data = {}
            today = datetime.today()

            data['cancel'] = AgentTransport.objects.filter(Q(date=today) & Q(status=0)).count()
            data['not_start'] = not_start = AgentTransport.objects.filter(Q(date=today) & Q(status=1)).count()
            data['pending'] = pending = AgentTransport.objects.filter(Q(date=today) & Q(status__in=[3,4])).count()
            data['completed'] = completed = AgentTransport.objects.filter(Q(date=today) & Q(status=2)).count()
            data['total'] = not_start + pending + completed

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_get_agent_transport_work_by_work_id(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads(request.body.decode('utf-8'))
            work_id = req['work_id']

            try:
                work = AgentTransport.objects.get(work_id=work_id)
                serializer = AgentTransportSerializer(work, many=False)
                data = serializer.data

            except AgentTransport.DoesNotExist:
                data = None

            return JsonResponse(data, safe=False)
    return JsonResponse('Error', safe=False)



