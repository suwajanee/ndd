from django.views.generic import TemplateView
from ..models import AgentTransport
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class AgentTransportUpdateView(TemplateView):
    @login_required(login_url=reverse_lazy('login'))
    def update_data_agent_transport(request):
        if request.method == 'POST':
            pk = request.POST['pk']
            address = request.POST['address'+pk]
            if address == 'other':
                address_other = request.POST['address_other']

            cancel = request.POST['cancel']

            filter_by = request.POST['filter_by']
            date_filter = request.POST['date_filter']

            agent_transport = AgentTransport.objects.get(pk=pk)
            agent_transport.address = address
            if address == 'other':
                agent_transport.address_other = address_other
            agent_transport.cancel = cancel
            agent_transport.save()

            messages.success(request, "Updated Agent Transport.")
            return redirect(reverse('agent-transport-table') + '?filter_by=' + filter_by + '&date=' + date_filter)
        else:
            return redirect('agent-transport-table')
