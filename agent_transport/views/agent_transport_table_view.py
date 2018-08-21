from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import AgentTransport
from ..forms import AgentTransportFilterSortForm
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class AgentTransportTableView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def get_table(request):
        template_name = 'agent_transport/agent_transport_table.html'

        today = datetime.now()

        if request.method == "GET":
            form = AgentTransportFilterSortForm(request.GET)
            date = request.GET.get("date")

            if date == None:
                date = ''

            if not date:
                agent_transports = AgentTransport.objects.filter(Q(date__month=today.month) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
            else:
                agent_transports = AgentTransport.objects.filter(Q(date=date) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
        else:
            agent_transports = AgentTransport.objects.filter(date__month=today.month | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')

        return render(request, template_name, {'agent_transports': agent_transports, 'form': form, 'date': date, 'today': today, 'nbar': 'agent-transport-table'})

    @login_required(login_url=reverse_lazy('login'))
    def delete_data(request, pk):
        agent_transport = AgentTransport.objects.get(pk=pk)
        agent_transport.delete()

        if request.method == "GET":
            date = request.GET.get("date")
            if not date:
                return redirect(reverse('agent-transport-table'))
            else:
                return redirect(reverse('agent-transport-table') + '?date=' + date)
    
    @login_required(login_url=reverse_lazy('login'))
    def update_data(request):
        if request.method == 'POST':
            pk = request.POST['pk']
            address = request.POST['address'+pk]
            if address == 'other':
                address_other = request.POST['address_other']

            cancel = request.POST['cancel']

            date_filter = request.POST['date_filter']

            agent_transport = AgentTransport.objects.get(pk=pk)
            agent_transport.address = address
            if address == 'other':
                agent_transport.address_other = address_other
            agent_transport.cancel = cancel
            agent_transport.save()

            messages.success(request, "Updated Agent Transport.")
            return redirect(reverse('agent-transport-table') + '?date=' + date_filter)
        else:
            return redirect('agent-transport-table')
