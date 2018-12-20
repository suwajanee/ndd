from django.contrib import admin
from .models import AgentTransport


class AgentTransportAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'pickup_tr', 'pickup_from', 'return_tr', 'return_to', \
    'container_1','container_2', 'remark', 'work_type', 'work_id', 'work_number', 'pickup_date', 'return_date')

    ordering = ('date', 'work_id')

    search_fields = ['work_id', 'container_1', 'container_2']

 
admin.site.register(AgentTransport, AgentTransportAdmin)