from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'time', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'start', 'pickup_tr', 'pickup_from', 'yard_ndd', 'forward_tr', \
    'factory', 'backward_tr', 'fac_ndd', 'return_tr', 'return_to', 'container_no','seal_no', 'tare',\
    'vessel', 'port', 'closing_date', 'closing_time', 'ref', 'remark', 'work_id', 'work_number', 'nextday', 'pickup_date', 'factory_date', 'return_date', 'pickup_in_time', 'pickup_out_time', \
    'factory_in_time', 'factory_load_start_time', 'factory_load_finish_time', 'factory_out_time', 'return_in_time', 'return_out_time')

    ordering = ('date', 'work_id')
 
admin.site.register(Booking, BookingAdmin)