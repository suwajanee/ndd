# -*- coding: utf-8 -*-

import re
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import AgentTransport
from .agent_transport_add_view import run_work_id
from .agent_transport_page_view import api_filter_agent_transports
from booking.views.utility.functions import check_key_detail
from customer.models import Shipper


@csrf_exempt
def api_save_edit_agent_transport(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            agent_transports = req['agent_transports']

            for agent_transport in agent_transports:
                if not agent_transport['date']:
                    agent_transport['date'] = None
                
                if not agent_transport['return_tr']:
                    agent_transport['return_tr'] = agent_transport['pickup_tr']

                if agent_transport['price'] == 'NaN':
                    agent_transport['price'] = 0

                agent_transport_save = AgentTransport.objects.get(pk=agent_transport['id'])

                if str(agent_transport_save.date) != agent_transport['date']:
                    work_id, work_number = run_work_id(agent_transport['date'], agent_transport_save.work_type)
                    agent_transport_save.work_id = work_id
                    agent_transport_save.work_number = work_number

                agent_transport_save.status = agent_transport['status']
                agent_transport_save.operation_type = agent_transport['operation_type']
                agent_transport_save.price = agent_transport['price']
                agent_transport_save.date = agent_transport['date']
                if agent_transport['shipper']:
                    agent_transport_save.shipper = Shipper.objects.get(pk=agent_transport['shipper']['id'])
                agent_transport_save.agent = re.sub(' +', ' ', agent_transport['agent'].strip().upper())
                agent_transport_save.size = re.sub(' +', ' ', agent_transport['size'].strip())
                agent_transport_save.booking_no = re.sub(' +', ' ', agent_transport['booking_no'].strip())
                agent_transport_save.pickup_tr = re.sub(' +', ' ', agent_transport['pickup_tr'].strip())
                agent_transport_save.pickup_from = re.sub(' +', ' ', agent_transport['pickup_from'].strip().upper())
                agent_transport_save.return_tr = re.sub(' +', ' ', agent_transport['return_tr'].strip())
                agent_transport_save.return_to = re.sub(' +', ' ', agent_transport['return_to'].strip().upper())
                agent_transport_save.container_1 = re.sub(' +', ' ', agent_transport['container_1'].strip())
                agent_transport_save.container_2 = re.sub(' +', ' ', agent_transport['container_2'].strip())
                agent_transport_save.remark = re.sub(' +', ' ', agent_transport['remark'].strip())          
                agent_transport_save.pickup_date = agent_transport['date']
                agent_transport_save.return_date = agent_transport['date']
                agent_transport_save.save()

        return api_filter_agent_transports(request)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_change_state_agent_transport(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            
            agent_transport_id = req['agent_transport_id']
            state = req['state']

            agent_transport = AgentTransport.objects.get(pk=agent_transport_id)
            if agent_transport.status == '3' and state == '3':
                state = '1'
            agent_transport.status = state
            agent_transport.save()

            return JsonResponse(agent_transport.status, safe=False)
    return JsonResponse('Error', safe=False)

@csrf_exempt
def api_change_color_field(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            
            agent_id = req['id']
            field = req['field']
            color = {field: req['color']}

            agent = AgentTransport.objects.get(pk=agent_id)
            if not agent.detail:
                agent.detail = {}
            agent.detail = check_key_detail(agent.detail, color, field, True)
            agent.save()

            if field in agent.detail:
                color_key = agent.detail[field]
            else:
                color_key = 0

            return JsonResponse(color_key, safe=False)
    return JsonResponse('Error', safe=False)
    
