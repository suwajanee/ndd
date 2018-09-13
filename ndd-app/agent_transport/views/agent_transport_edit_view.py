from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import AgentTransport


class AgentTransportEditTableView(TemplateView):
    
    @login_required(login_url=reverse_lazy('login'))
    def render_edit_agent_transport_page(request):
        template_name = 'agent_transport/agent_transport_edit.html'
        context = {}
        context['nbar'] = 'agent-transport-table'
        context['today'] = datetime.now()  

        if request.method == "GET":
            context['filter_by'] = request.GET.get("filter_by")
            context['date_filter'] = request.GET.get("date_filter")

            if context['date_filter'] == None:
                context['date_filter'] = ''

            if not context['date_filter']:
                context['agent_transports'] = AgentTransport.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
            else:
                if context['filter_by'] == "month":
                    month_of_year = datetime.strptime(context['date_filter'], '%Y-%m')
                    context['agent_transports'] = AgentTransport.objects.filter((Q(date__month=month_of_year.month) & Q(date__year=month_of_year.year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
                else:
                    context['agent_transports'] = AgentTransport.objects.filter(Q(date=context['date_filter']) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')
        else:
            context['agent_transports'] = AgentTransport.objects.filter((Q(date__month=context['today'].month) & Q(date__year=context['today'].year)) | (Q(return_tr='') & Q(cancel=0))).order_by('date', 'work_id')

        return render(request, template_name, context)        

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
                agent_transport.size = size[i].strip()
                agent_transport.booking_no = booking_no[i].strip()
                agent_transport.pickup_tr = pickup_tr[i].strip()
                agent_transport.pickup_from = pickup_from[i].strip()
                agent_transport.return_tr = return_tr[i].strip()
                agent_transport.return_to = return_to[i].strip()
                agent_transport.container_1 = container_1[i].strip()
                agent_transport.container_2 = container_2[i].strip()
                agent_transport.ref = ref[i].strip()
                agent_transport.remark = remark[i].strip()
                agent_transport.pickup_date = pickup_date[i]
                agent_transport.return_date = return_date[i]
                agent_transport.save()

            messages.success(request, "Saving Agent Transport.")
            return redirect(reverse('agent-transport-edit') + '?filter_by=' + filter_by + '&date_filter=' + date_filter)
        else:
            return redirect('agent-transport-edit')
