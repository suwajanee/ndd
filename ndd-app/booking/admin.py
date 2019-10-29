from django.contrib import admin
from .models import Booking
from .models import BookingTime
from .models import ContainerSize


class BookingAdmin(admin.ModelAdmin):
    list_display = ('date', 'status', 'time', 'principal', 'shipper', 'agent', 'size', 'booking_no', 'pickup_tr', 'pickup_from', 'yard_ndd', 'forward_tr', \
    'factory', 'backward_tr', 'fac_ndd', 'return_tr', 'return_to', 'container_no','seal_no', 'tare',\
    'vessel', 'port', 'closing_date', 'closing_time', 'remark', 'work_id', 'work_number', 'nextday', 'pickup_date', 'factory_date', 'return_date', 'detail', 'summary_status')

    ordering = ('date', 'principal__name', 'shipper__name', 'booking_no', 'work_id')

    search_fields = ['work_id', 'booking_no', 'container_no']


class BookingTimeAdmin(admin.ModelAdmin):
    list_display = ('booking', 'key', 'time')

    ordering = ('booking__work_id', 'key')

    search_fields = ['booking__work_id']


class ContainerSizeAdmin(admin.ModelAdmin):
    list_display = ('get_container',)
    def get_container(self, obj):
        if obj.num == '2':
            return obj.num + 'X' + obj.size
        else:
            return obj.size

    get_container.short_description = 'Container Size'
    
 
admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingTime, BookingTimeAdmin)
admin.site.register(ContainerSize, ContainerSizeAdmin)
