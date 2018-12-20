# -*- coding: utf-8 -*-

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import AgentTransport
from .agent_transport_page_view import api_filter_agent_transports


@csrf_exempt
def api_delete_agent_transports(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            pk_list = req["checked_agent_transports"]

            for pk in pk_list:
                agent_transport = AgentTransport.objects.get(pk=pk)
                agent_transport.delete()

        return api_filter_agent_transports(request)
    return JsonResponse('Error', safe=False)
    
