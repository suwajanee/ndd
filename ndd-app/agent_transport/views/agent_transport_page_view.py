# -*- coding: utf-8 -*-

from datetime import datetime
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Case, When
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from ..models import AgentTransport
from ..serializers import AgentTransportSerializer


@login_required(login_url=reverse_lazy('login'))
def agent_transport_page(request):
    return render(request, 'agent_transport/agent_transport_page.html', {'nbar': 'agent-transport-page'})

@csrf_exempt
def api_filter_agent_transports(request):
    if request.user.is_authenticated:
        context = {}
        context['today'] = datetime.now()

        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            filter_by = req['filter_by']
            date_filter = req['date_filter']
            if date_filter == '':
                date_filter = None

            if date_filter == None:
                agent_transports = AgentTransport.objects.filter(Q(date=context['today']) | Q(status__in=[1,3])).order_by('date', 'principal__name', 'shipper__name', 'work_type', \
                Case(
                    When(work_type='ep', then='booking_no'),
                ), 'work_id')
            elif filter_by == "month":
                month_of_year = datetime.strptime(date_filter, '%Y-%m')
                agent_transports = AgentTransport.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | Q(status__in=[1,3])).order_by('date', 'principal__name', 'shipper__name', 'work_type', \
                Case(
                    When(work_type='ep', then='booking_no'),
                ), 'work_id')
            else:
                agent_transports = AgentTransport.objects.filter(Q(date=date_filter) | Q(status__in=[1,3])).order_by('date', 'principal__name', 'shipper__name', 'work_type', \
                Case(
                    When(work_type='ep', then='booking_no'),
                ), 'work_id')

        else:
            agent_transports = AgentTransport.objects.filter(Q(date=context['today']) | Q(status__in=[1,3])).order_by('date', 'principal__name', 'shipper__name', 'work_type', \
            Case(
                    When(work_type='ep', then='booking_no'),
                ), 'work_id')
            
        serializer = AgentTransportSerializer(agent_transports, many=True)
        context['agent_transports'] = serializer.data
        return JsonResponse(context, safe=False)
    return JsonResponse('Error', safe=False)
