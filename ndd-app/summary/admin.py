from django.contrib import admin
from .models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail, InvoiceSetting


class YearAdmin(admin.ModelAdmin):
    list_display = ('year_label', )


class FormDetailAdmin(admin.ModelAdmin):
    list_display = ('form_name', 'form_detail')


class CustomerCustomAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sub_customer', 'customer_title', 'form', 'option')
    ordering = ('customer', 'sub_customer')

    search_fields = ['customer__name',]


class SummaryWeekAdmin(admin.ModelAdmin):
    list_display = ('week', 'month', 'year', 'date_start', 'date_end', 'diesel_rate', 'status')
    ordering = ('week', )

    search_fields = ['week', 'year__year_label']


class SummaryCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'week', 'date_billing', 'date_end', 'detail', 'status')
    ordering = ('week',)

    search_fields = ['customer_main__name', 'customer_custom__customer__name', 'week__week']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer_week', 'drayage_total', 'gate_total', 'status', 'detail')
    ordering = ('customer_week__week__year', 'customer_week__week', 'invoice_no')

    search_fields = ['invoice_no']


class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'work', 'drayage_charge', 'gate_charge', 'detail')
    ordering = ('invoice', )

    search_fields = ['invoice__invoice_no', 'work_normal__booking_no', 'work_agent_transport__booking_no', 'work_normal__work_id', 'work_agent_transport__work_id']


class InvoiceSettingAdmin(admin.ModelAdmin):
    list_display = ('primary', 'data')
    ordering = ('primary', )


admin.site.register(Year, YearAdmin)
admin.site.register(FormDetail, FormDetailAdmin)
admin.site.register(CustomerCustom, CustomerCustomAdmin)
admin.site.register(SummaryWeek, SummaryWeekAdmin)
admin.site.register(SummaryCustomer, SummaryCustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)
admin.site.register(InvoiceSetting, InvoiceSettingAdmin)
