from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import AgentTransport


class AgentTransportTableView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def render_table_agent_transport_page(request):
        template_name = 'agent_transport/agent_transport_table.html'

        today = datetime.now()

        if request.method == "GET":
            filter_by = request.GET.get("filter_by")
            date_filter = request.GET.get("date_filter")

            if date_filter == None:
                date_filter = ''

            if not date_filter:
                agent_transports = AgentTransport.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
            else:
                if filter_by == "month":
                    month_of_year = datetime.strptime(date_filter, '%Y-%m')
                    agent_transports = AgentTransport.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
                else:
                    agent_transports = AgentTransport.objects.filter(Q(date=date_filter) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
        else:
            agent_transports = AgentTransport.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')

        return render(request, template_name, {'agent_transports': agent_transports, 'filter_by': filter_by, 'date_filter': date_filter, 'today': today, 'nbar': 'agent-transport-table'})
    

   