# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy

from ..models import Employee
from ..serializers import EmployeeSerializer


@login_required(login_url=reverse_lazy('login'))
def employee_page(request):
    return render(request, 'employee/employee_page.html', {'nbar': 'database-page'})

@csrf_exempt
def api_get_employee(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            req = json.loads( request.body.decode('utf-8') )

            employee = Employee.objects.all().order_by('cancel', 'name')

        serializer = EmployeeSerializer(employee, many=True)

        return JsonResponse(serializer.data, safe=False)
    return JsonResponse('Error', safe=False) 