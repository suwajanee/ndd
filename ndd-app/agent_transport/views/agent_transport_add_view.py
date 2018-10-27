# -*- coding: utf-8 -*-

import re
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Q
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..forms import AgentTransportAddForm
from ..models import AgentTransport
from customer.models import Principal, Shipper


class AgentTransportAddView(TemplateView):

    @login_required(login_url=reverse_lazy('login'))
    def render_add_agent_transport_page(request):
        add_agent_transport = AgentTransportAddView()
        template_name = 'agent_transport/agent_transport_add.html'
        context = {}
        context['form'] = AgentTransportAddForm()
        context['principals'] = Principal.objects.filter(Q(work_type='agent-transport') & Q(cancel=0)).order_by('name')
        context['nbar'] = 'agent-transport-table'
        if request.method == 'POST':
            context = add_agent_transport.create_context(request.POST)
            
        return render(request, template_name, context)

    def create_context(self, req):
        context = {}
        context['principals'] = Principal.objects.filter(Q(work_type='agent-transport') & Q(cancel=0)).order_by('name')
        context['nbar'] = 'agent-transport-table'
        if 'principal' in req:
            context['principal'] = req.get('principal')
            if context['principal']:
                context['shippers'] = Shipper.objects.filter(Q(principal=context['principal']) & Q(cancel=0)).order_by('name')
                context['principal_name'] = Principal.objects.get(pk=context['principal']).name
            else:
                context['shippers'] = []
            req._mutable = True
            context['size_list'] = req.getlist('size')
            context['quantity_list'] = req.getlist('quantity')
            context['date_list'] = req.getlist('date')
            context['zip'] = zip(context['size_list'], context['quantity_list'], context['date_list'])

            req.update({'size':'', 'quantity':'', 'date':''})
            context['form'] = AgentTransportAddForm(req)
        return context

    @login_required(login_url=reverse_lazy('login'))
    def save_data_agent_transport(request):
        add_agent_transport = AgentTransportAddView()
        if request.method == 'POST':
            form = AgentTransportAddForm(request.POST)
            if form.is_valid():
                principal = request.POST['principal']
                shipper = request.POST['shipper']
                agent = request.POST['agent']
                booking_no = request.POST['booking_no']
                work_type = request.POST['work_type']
                size_list = request.POST.getlist('size')
                quantity_list = request.POST.getlist('quantity')
                date_list = request.POST.getlist('date')
                pickup_from = request.POST['pickup_from']
                return_to = request.POST['return_to']
                remark = request.POST['remark']

                container = zip(size_list, quantity_list, date_list)
                for size, quantity, date in container:

                    for i in range(int(quantity)):
                        work_id, work_number = add_agent_transport.run_work_id(date, work_type)
                        data = {
                            'principal': Principal.objects.get(pk=principal),
                            'shipper': Shipper.objects.get(pk=shipper),
                            'agent': re.sub(' +', ' ', agent.strip().upper()),
                            'booking_no': re.sub(' +', ' ', booking_no.strip()),
                            'work_type': work_type,
                            'size': re.sub(' +', ' ', size.strip()),
                            'date': date,
                            'pickup_from': re.sub(' +', ' ', pickup_from.strip().upper()),
                            'return_to': re.sub(' +', ' ', return_to.strip().upper()),
                            'remark': re.sub(' +', ' ', remark.strip()),
                            'work_id': work_id,
                            'work_number': work_number,
                            'pickup_date': date,
                            'return_date': date,
                        }

                        agent_transport = AgentTransport(**data)
                        agent_transport.save()
                 
                return redirect('agent-transport-page')
            messages.error(request, "Form not validate.")
        return redirect('agent-transport-add')

    def run_work_id(self, date, work_type):
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
