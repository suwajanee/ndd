from django.contrib import admin
from .models import Manufacturer
from .models import Truck
from .models import Chassis

# Register your models here.
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', )
    ordering = ('-category', 'name')


class TruckAdmin(admin.ModelAdmin):
    list_display = ('number', 'license_plate', 'manufacturer', 'driver', 'tax_expired_date', 'pat_pass_expired_date', 'status')
    ordering = ('number', )


class ChassisAdmin(admin.ModelAdmin):
    list_display = ('number', 'license_plate', 'manufacturer', 'tax_expired_date', 'status')
    ordering = ('number', )


admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(Chassis, ChassisAdmin)
