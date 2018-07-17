from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display= ('date', 'time', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'booking_color', 'fw_tr', 'fw_fm', 'container_no','seal_no', 'bw_tr', \
    'bw_to', 'vessel', 'port', 'closing_time', 'remark', 'loading', 'work_id', 'pickup_date', 'factory_date', 'return_date', 'pickup_out_time', \
    'factory_in_time', 'factory_load_start_time', 'factory_load_finish_time', 'factory_out_finish', 'return_in_time', 'return_out_time', \
    'address', 'address_other')
    
admin.site.register(Booking, BookingAdmin)
