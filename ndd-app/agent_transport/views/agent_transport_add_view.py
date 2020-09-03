# -*- coding: utf-8 -*-

from datetime import datetime
import json
import re

from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import AgentTransport
from ..serializers import AgentTransportSerializer
from customer.models import Principal, Shipper


@login_required(login_url=reverse_lazy('login'))
def agent_trnasport_add_page(request):
    return render(request, 'agent_transport/agent_transport_add_page.html', {'nbar': 'agent-transport-page'})

@csrf_exempt
def api_save_add_agent_transports(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )

            agent_transports = req['agent_transports']
            details = req['details']

            agent_transports['principal'] = Principal.objects.get(pk=agent_transports['principal'])
            agent_transports['shipper'] = Shipper.objects.get(pk=agent_transports['shipper'])
            agent_transports['agent'] = re.sub(' +', ' ', agent_transports['agent'].strip().upper())
            agent_transports['booking_no'] = re.sub(' +', ' ', agent_transports['booking_no'].strip())

            agent_transports['pickup_from'] = re.sub(' +', ' ', agent_transports['pickup_from'].strip().upper())
            agent_transports['return_to'] = re.sub(' +', ' ', agent_transports['return_to'].strip().upper())

            agent_transports['remark'] = re.sub(' +', ' ', agent_transports['remark'].strip())

            if agent_transports['price'] == 'NaN':
                agent_transports['price'] = 0

            if agent_transports['operation_type'] == 'export_empty' or agent_transports['operation_type'] == 'import_empty':
                work_type = 'ep'
            else:
                work_type = 'fc'
            
            for detail in details:
                agent_transports['date'] = detail['date']
                agent_transports['pickup_date'] = detail['date']
                agent_transports['return_date'] = detail['date']

                agent_transports['size'] = detail['size']

                agent_transports['container_1'] = ''
                agent_transports['container_2'] = ''

                if detail['container_input'] == False:
                    for i in range(int(detail['quantity'])):
                        work_id, work_number = run_work_id(detail['date'], work_type)

                        agent_transports['work_id'] = work_id
                        agent_transports['work_number'] = work_number

                        agent_transport = AgentTransport(**agent_transports)
                        agent_transport.save()
                else:
                    for cont_detail in detail['container']:
                        agent_transports['container_1'] = cont_detail['container_1']
                        agent_transports['container_2'] = cont_detail['container_2']

                        work_id, work_number = run_work_id(detail['date'], work_type)

                        agent_transports['work_id'] = work_id
                        agent_transports['work_number'] = work_number

                        agent_transport = AgentTransport(**agent_transports)
                        agent_transport.save()

            return JsonResponse('Success', safe=False)

    return JsonResponse('Error', safe=False)

def run_work_id(date, work_type):
    work = AgentTransport.objects.filter(date=date, work_type=work_type).aggregate(Max('work_number'))
    if work['work_number__max'] == None:
        work_number = 1
    else:
        work_number = work['work_number__max'] + 1

    work = str("{:03d}".format(work_number))
    date = datetime.strptime(date, "%Y-%m-%d")
    work_id = work_type.upper()+date.strftime('%d%m%y') + work

    while True:
        exist_id = AgentTransport.objects.filter(work_id=work_id)
        if exist_id:
            work_number = work_number + 1
            work = str("{:03d}".format(work_number))
            work_id = work_type.upper()+date.strftime('%d%m%y') + work
        else:
            break

    return work_id, work_number
    