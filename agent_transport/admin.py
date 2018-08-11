from django.contrib import admin
from .models import AgentTransport


class AgentTransportAdmin(admin.ModelAdmin):
    list_display = ('date', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'booking_color', 'pickup_tr', 'pickup_from', 'return_tr', 'return_to', \
    'container_1','container_1', 'ref', 'remark', 'work_type', 'work_id', 'work_number', 'pickup_date', 'return_date', 'address', 'address_other', 'cancel')
 
admin.site.register(AgentTransport, AgentTransportAdmin)