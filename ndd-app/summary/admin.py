from django.contrib import admin
from .models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail


class YearAdmin(admin.ModelAdmin):
    list_display = ('year_label', )


class FormDetailAdmin(admin.ModelAdmin):
    list_display = ('form_name', 'form_detail')


class CustomerCustomAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sub_customer', 'customer_title', 'form', 'option')
    ordering = ('customer', 'sub_customer')


class SummaryWeekAdmin(admin.ModelAdmin):
    list_display = ('week', 'month', 'year', 'date_start', 'date_end', 'diesel_rate', 'status')
    ordering = ('week', )


class SummaryCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'week', 'date_billing', 'date_end', 'detail', 'status')
    ordering = ('week',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer_week', 'drayage_total', 'gate_total', 'status', 'detail')
    ordering = ('customer_week__week__year', 'customer_week__week', 'invoice_no')


class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'work', 'drayage_charge', 'gate_charge', 'detail')
    ordering = ('invoice', )


admin.site.register(Year, YearAdmin)
admin.site.register(FormDetail, FormDetailAdmin)
admin.site.register(CustomerCustom, CustomerCustomAdmin)
admin.site.register(SummaryWeek, SummaryWeekAdmin)
admin.site.register(SummaryCustomer, SummaryCustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)