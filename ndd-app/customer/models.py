from django.db import models

# Create your models here.

class Principal(models.Model):
    name = models.CharField(max_length=200, blank=True)
    WORK_CHOICES = (
        ('normal', 'Normal'),
        ('agent-transport', 'Agent Transport'),
    )
    work_type = models.CharField(max_length=20, choices=WORK_CHOICES, default='normal')
    CANCEL_CHOICES = (
        ('1', 'Cancel'),
        ('0', '-'),
    )
    cancel = models.CharField(max_length=1, choices=CANCEL_CHOICES, default=0)

    def __str__(self):
        return self.name


class Shipper(models.Model):
    principal = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name="shippers")
    name = models.CharField(max_length=200, blank=True, default='')
    address = models.CharField(max_length=500, blank=True, default='')
    CANCEL_CHOICES = (
        ('1', 'Cancel'),
        ('0', '-'),
    )
    cancel = models.CharField(max_length=1, choices=CANCEL_CHOICES, default=0)

    def __str__(self):
        return self.name


class ShipperAddress(models.Model):
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, blank=True)
    address_type = models.CharField(max_length=50, blank=True, default='')
    address = models.CharField(max_length=500, blank=True, default='')