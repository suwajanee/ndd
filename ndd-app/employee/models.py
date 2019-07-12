from django.contrib.postgres.fields import JSONField
from django.db import models

# Create your models here.

class Job(models.Model):
    job_title = models.CharField(max_length=15, blank=True, null=True, default='')

    def __str__(self) :
        return self.job_title


class Employee(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True, default='')
    last_name = models.CharField(max_length=50, blank=True, null=True, default='')
    birth_date = models.DateField(blank=True, null=True, default=None)
    hire_date = models.DateField(blank=True, null=True, default=None)
    status = models.CharField(max_length=100, blank=True, null=True, default='')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, blank=True)
    detail = JSONField(null=True, blank=True, default=dict)

    def __str__(self) :
        return self.first_name + ' ' + self.last_name


class Driver(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    license_type = models.CharField(max_length=1, blank=True, null=True, default='')
    pat_pass_expired_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self) :
        if self.employee:
            return self.employee.first_name + ' ' + self.employee.last_name
        else:
            return str(self.pk)


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    from_date = models.DateField(blank=True, null=True, default=None)
    to_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self) :
        if self.employee:
            return self.employee.first_name + ' ' + self.employee.last_name
        else:
            return str(self.pk)