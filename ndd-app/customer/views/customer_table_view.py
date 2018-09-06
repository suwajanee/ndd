from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..models import Principal, Shipper


class CustomerListView(TemplateView):

    global template_name
    template_name = 'customer/customer_table.html'

    @login_required(login_url=reverse_lazy('login'))
    def render_customer_list(request):
        principals = Principal.objects.all().order_by('name')
        return render(request, template_name, {'principals': principals, 'nbar': 'customer'})

    @login_required(login_url=reverse_lazy('login'))
    def render_customer_detail(request, pk):
        principals = Principal.objects.all().order_by('name')

        customer = Principal.objects.get(pk=pk)
        shippers = Shipper.objects.filter(principal=pk).order_by('name')

        return render(request, template_name, {'principals': principals, 'customer': customer, 'shippers': shippers, 'nbar': 'customer'})

