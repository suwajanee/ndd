from django.contrib import admin
from .models import Year, FormDetail, CustomerForm, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail


class YearAdmin(admin.ModelAdmin):
    list_display = ('name', )


class FormDetailAdmin(admin.ModelAdmin):
    list_display = ('form_name', 'form_detail')


class CustomerFormAdmin(admin.ModelAdmin):
    list_display = ('customer', 'sub_customer', 'customer_title', 'form', 'optional')
    ordering = ('customer', 'sub_customer')


class SummaryWeekAdmin(admin.ModelAdmin):
    list_display = ('week', 'month', 'year', 'date_start', 'date_end', 'diesel_rate_of_week', 'status')
    ordering = ('week', )


class SummaryCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer', 'week', 'date_billing', 'date_end', 'status')
    ordering = ('week', 'customer')


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_no', 'customer_week', 'total', 'status')
    ordering = ('customer_week__week__year', 'customer_week__week', 'invoice_no')


class InvoiceDetailAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'work')
    # ordering = ('invoice', )


admin.site.register(Year, YearAdmin)
admin.site.register(FormDetail, FormDetailAdmin)
admin.site.register(CustomerForm, CustomerFormAdmin)
admin.site.register(SummaryWeek, SummaryWeekAdmin)
admin.site.register(SummaryCustomer, SummaryCustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceDetail, InvoiceDetailAdmin)