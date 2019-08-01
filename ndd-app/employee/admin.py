from django.contrib import admin
from .models import Driver
from .models import Employee
from .models import Job
from .models import Salary

# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'number', 'starting_salary')
    ordering = ('number',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'hire_date', 'job', 'detail', 'status')
    ordering = ('job__number', 'first_name', 'last_name')
    search_fields = ['first_name', 'last_name']


class DriverAdmin(admin.ModelAdmin):
    list_display = ('employee', 'license_type', 'pat_pass_expired_date')
    ordering = ('employee__first_name', 'employee__last_name')


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'salary', 'from_date', 'to_date')
    ordering = ('employee__job__number', 'employee__first_name', 'employee__last_name')


admin.site.register(Job, JobAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Salary, SalaryAdmin)
