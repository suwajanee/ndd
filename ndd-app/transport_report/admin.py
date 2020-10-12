from django.contrib import admin

from .models import WorkOrder
from .models import Expense
from .models import ExpenseSummaryDate
from .models import Variable


class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('clear_date', 'work_date', 'work', 'order_type', 'double_container', 'driver', 'truck', 'detail', 'price')
    ordering = ('clear_date', 'truck__number', 'work_date')

    search_fields = ['clear_date', 'work_normal__work_id', 'work_agent_transport__work_id', 'driver__employee__first_name']


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('work_order', 'co_expense', 'cus_expense', 'co_total', 'cus_total')
    ordering = ('work_order__clear_date', 'work_order__truck__number', 'work_order__work_date')

    search_fields = ['work_order__clear_date', 'work_order__work_normal__work_id', 'work_order__work_agent_transport__work_id', 'work_order__driver__employee__first_name']


class ExpenseSummaryDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'month', 'year')
    ordering = ('-date')


class VariableAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    ordering = ('key',)


admin.site.register(WorkOrder, WorkOrderAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(ExpenseSummaryDate, ExpenseSummaryDateAdmin)
admin.site.register(Variable, VariableAdmin)
