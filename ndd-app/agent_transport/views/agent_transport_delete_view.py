# -*- coding: utf-8 -*-

import decimal
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import AgentTransport
from .agent_transport_page_view import api_get_agent_transports
from summary.models import InvoiceDetail


@csrf_exempt
def api_delete_agent_transports(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            pk_list = req["checked_agent_transports"]

            for pk in pk_list:
                agent_transport = AgentTransport.objects.get(pk=pk)

                details = InvoiceDetail.objects.filter(work_agent_transport=agent_transport)
                for detail in details:
                    if detail.drayage_charge['drayage']:
                        detail.invoice.drayage_total -= decimal.Decimal(eval(detail.drayage_charge['drayage']))
                    if 'other' in detail.drayage_charge:
                        for other in detail.drayage_charge['other']:
                            if other['other_charge']:
                                detail.invoice.drayage_total -= decimal.Decimal(eval(other['other_charge']))
                    if  detail.gate_charge:
                        if detail.gate_charge['gate']:
                            detail.invoice.gate_total -= decimal.Decimal(eval(detail.gate_charge['gate']))

                    detail.invoice.save()
                    detail.delete()
                agent_transport.delete()

        return api_get_agent_transports(request)
    return JsonResponse('Error', safe=False)
    
