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
        context = {}
        context['nbar'] = 'agent-transport-table'
        context['today'] = datetime.now()

        if request.method == "GET":
            context['filter_by'] = request.GET.get("filter_by")
            context['date_filter'] = request.GET.get("date_filter")

            if context['date_filter'] == None:
                context['date_filter'] = ''

            if not context['date_filter']:
                context['agent_transports'] = AgentTransport.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | Q(status=1)).order_by('date', 'shipper', 'work_id')
            else:
                if context['filter_by'] == "month":
                    month_of_year = datetime.strptime(context['date_filter'], '%Y-%m')
                    context['agent_transports'] = AgentTransport.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | Q(status=1)).order_by('date', 'shipper', 'work_id')
                else:
                    context['agent_transports'] = AgentTransport.objects.filter(Q(date=context['date_filter']) | Q(status=1)).order_by('date', 'shipper', 'work_id')
        else:
            context['agent_transports'] = AgentTransport.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | Q(status=1)).order_by('date', 'shipper', 'work_id')

        return render(request, template_name, context)
    

   