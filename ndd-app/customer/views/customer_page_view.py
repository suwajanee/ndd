import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url=reverse_lazy('login'))
def customer_page(request):
    return render(request, 'customer/customer_page.html', {'nbar': 'customer-page'})