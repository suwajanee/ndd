# -*- coding: utf-8 -*-

import copy
import json
import re

from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Year, CustomerCustom, SummaryWeek, Invoice
from customer.models import Principal
from ..serializers import SummaryWeekSerializer


@csrf_exempt
def api_get_summary_month_details(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            req = json.loads( request.body.decode('utf-8') )
            year = req['year']
            month = req['month']

            details = {}

            year_existing = Year.objects.filter(year_label=year)
            if not year_existing or int(month) not in range(1,13) :
                return JsonResponse('Error', safe=False)

            summary_month_details = []
            color_list = ['#e0ffff', '#cefdce', '#ffffff']
            color_index = 0

            customers = Principal.objects.all().order_by('name')

            # get weeks data
            week_details = SummaryWeek.objects.filter(Q(year__year_label=year) & Q(month=month)).order_by('week')
            week_serializer = SummaryWeekSerializer(week_details, many=True)
            weeks = details['weeks'] = week_serializer.data

            for customer in customers:
                data = {}
                total = []
                data['customer'] = customer.name
                data['color'] = color_list[color_index % 3]
                color_index += 1
                sub_customers = CustomerCustom.objects.filter(Q(customer__name=customer.name)).order_by('customer__name','sub_customer')
                if sub_customers:
                    customer_total = 0
                    last_index = 0
                    for sub_customer in sub_customers:
                        data = copy.deepcopy(data)
                        data['sub_customer'] = sub_customer.sub_customer
                        total = []
                        for week in weeks:
                            week_total = Invoice.objects.filter(Q(customer_week__week=week['id']) & \
                                            Q(customer_week__customer_custom = sub_customer) & \
                                            Q(customer_week__customer_custom__sub_customer = sub_customer.sub_customer)).aggregate(total=Sum('drayage_total'))['total']

                            if week_total:
                                total.append(float(week_total))
                                customer_total += float(week_total)
                            else:
                                total.append(None)

                            data['total'] = total

                        if last_index == len(sub_customers)-1:
                            data['cusotomer_total'] = customer_total
                            customer_total = 0
                            last_index = 0
                        
                        last_index += 1

                        summary_month_details.append(data)
                else:
                    for week in weeks:
                        week_total = Invoice.objects.filter(Q(customer_week__week=week['id']) & \
                                        Q(customer_week__customer_main__name = customer.name)).aggregate(total=Sum('drayage_total'))['total']

                        if week_total:
                            total.append(float(week_total))
                        else:
                            total.append(None)

                        data['total'] = total
                    summary_month_details.append(data)
            details['summary_month_details'] = summary_month_details
            return JsonResponse(details, safe=False)
    return JsonResponse('Error', safe=False)
