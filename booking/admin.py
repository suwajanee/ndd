from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display= ('time', 'date', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'fw_tr', 'fw_fm', 'container_no','seal_no', 'bw_tr', \
    'bw_to', 'vessel', 'port', 'closing_time', 'remark', 'loading', 'work_id', 'pickup_date', 'factory_date', 'return_date')
    
admin.site.register(Booking, BookingAdmin)
