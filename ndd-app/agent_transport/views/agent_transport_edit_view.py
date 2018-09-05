from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..forms import AgentTransportFilterSortForm
from ..models import AgentTransport


class AgentTransportEditTableView(TemplateView):
    
    @login_required(login_url=reverse_lazy('login'))
    def render_edit_agent_transport(request):
        template_name = 'agent_transport/agent_transport_edit.html'

        today = datetime.now()

        if request.method == "GET":
            filter_by = request.GET.get("filter_by")
            date_filter = request.GET.get("date_filter")

            if date_filter == None:
                date_filter = ''

            if not date_filter:
                agent_transports = AgentTransport.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
            else:
                if filter_by == "month":
                    month_year = datetime.strptime(date_filter, '%Y-%m')
                    agent_transports = AgentTransport.objects.filter((Q(date__month=month_year.month) & Q(date__year=month_year.year)) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
                else:
                    agent_transports = AgentTransport.objects.filter(Q(date=date_filter) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')
        else:
            agent_transports = AgentTransport.objects.filter((Q(date__month=today.month) & Q(date__year=today.year)) | (Q(return_tr='') & ~Q(cancel='1'))).order_by('date', 'work_id')

        return render(request, template_name, {'agent_transports': agent_transports, 'filter_by': filter_by, 'date_filter': date_filter, 'today': today, 'nbar': 'agent-transport-table'})


    @login_required(login_url=reverse_lazy('login'))
    def save_edit_data_agent_transport(request):
        if request.method == 'POST':
            pk = request.POST.getlist('pk')
            date = request.POST.getlist('date')
            size = request.POST.getlist('size')
            booking_no = request.POST.getlist('booking_no')
            pickup_tr = request.POST.getlist('pickup_tr')
            pickup_from = request.POST.getlist('pickup_from')
            return_tr = request.POST.getlist('return_tr')
            return_to = request.POST.getlist('return_to')
            container_1 = request.POST.getlist('container_1')
            container_2 = request.POST.getlist('container_2')
            ref = request.POST.getlist('ref')
            remark = request.POST.getlist('remark')
            pickup_date = request.POST.getlist('pickup_date')
            return_date = request.POST.getlist('return_date')

            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            for i in range(len(pk)):
    
                if not date[i]:
                    date[i] = None
                if not pickup_date[i]:
                    pickup_date[i] = None
                if not return_date[i]:
                    return_date[i] = None

                agent_transport = AgentTransport.objects.get(pk=pk[i])
                agent_transport.date = date[i]
                agent_transport.size = size[i]
                agent_transport.booking_no = booking_no[i]
                agent_transport.pickup_tr = pickup_tr[i]
                agent_transport.pickup_from = pickup_from[i]
                agent_transport.return_tr = return_tr[i]
                agent_transport.return_to = return_to[i]
                agent_transport.container_1 = container_1[i]
                agent_transport.container_2 = container_2[i]
                agent_transport.ref = ref[i]
                agent_transport.remark = remark[i]
                agent_transport.pickup_date = pickup_date[i]
                agent_transport.return_date = return_date[i]
                agent_transport.save()

            messages.success(request, "Saving Agent Transport.")
            return redirect(reverse('agent-transport-edit') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)
        else:
            return redirect('agent-transport-edit')
