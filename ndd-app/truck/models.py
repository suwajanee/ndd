from django.db import models

from employee.models import Driver
# Create your models here.

class TruckManufacturer(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    category = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        if self.category:
            return self.name + ' (' + self.category + ')'
        return self.name


class Truck(models.Model):
    number = models.CharField(max_length=5, blank=True, null=True)
    license_plate = models.CharField(max_length=7, blank=True, null=True)
    manufacturer = models.ForeignKey(TruckManufacturer, on_delete=models.SET_NULL, blank=True, null=True)

    driver = models.OneToOneField(Driver, on_delete=models.SET_NULL, blank=True, null=True)
    
    tax_expired_date = models.DateField(blank=True, null=True, default=None)
    pat_pass_expired_date = models.DateField(blank=True, null=True, default=None)

    status = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.number


class Chassis(models.Model):
    number = models.CharField(max_length=3, blank=True, null=True)
    license_plate = models.CharField(max_length=7, blank=True, null=True)
    tax_expired_date = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return self.number
