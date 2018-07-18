from django.contrib import admin
from .models import Principal
from .models import Shipper

# Register your models here.
class PrincipalAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ShipperAdmin(admin.ModelAdmin):
    list_display = ('principal', 'name', 'address')

admin.site.register(Principal, PrincipalAdmin)
admin.site.register(Shipper, ShipperAdmin)