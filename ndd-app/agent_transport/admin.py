from django.contrib import admin
from .models import AgentTransport


class AgentTransportAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'pickup_tr', 'pickup_from', 'yard_ndd', 'return_tr', 'return_to', \
    'container_1','container_2', 'remark', 'work_type', 'operation_type', 'price', 'work_id', 'work_number', 'pickup_date', 'return_date', 'detail', 'summary_status')

    ordering = ('date', 'principal__name', 'shipper__name', 'work_type', 'booking_no', 'work_id')

    search_fields = ['work_id', 'booking_no', 'container_1', 'container_2']
 
admin.site.register(AgentTransport, AgentTransportAdmin)