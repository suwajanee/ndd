from django.contrib.postgres.fields import JSONField
from django.db import models
from datetime import datetime
from customer.models import Principal, Shipper

# Create your models here.

class AgentTransport(models.Model):
    date = models.DateField(default=datetime.now, null=True)
    principal = models.ForeignKey(Principal, on_delete=models.SET_NULL, null=True, blank=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=15, blank=True)
    booking_no = models.CharField(max_length=120, blank=True)

    NDD_CHOICES = (
        ('2', 'Yard'),
        ('1', 'NDD'),
        ('0', '-'),
    )
    pickup_tr = models.CharField(max_length=15, blank=True, default='')
    pickup_from = models.CharField(max_length=25, blank=True, default='')

    yard_ndd = models.CharField(max_length=1, choices=NDD_CHOICES, default=0)

    return_tr = models.CharField(max_length=15, blank=True, default='')
    return_to = models.CharField(max_length=25, blank=True, default='')

    container_1 = models.CharField(max_length=25, blank=True, default='')
    container_2 = models.CharField(max_length=25, blank=True, default='')
    remark = models.TextField(blank=True, default='')
    
    WORK_CHOICES = (
        ('ep', 'Empty'),
        ('fc', 'Full'),
    )
    work_type = models.CharField(max_length=2, choices=WORK_CHOICES, default='ep')

    OPERATION_CHOICES = (
        ('', '-'),
        ('export_loaded', 'Export Loaded'),
        ('import_loaded', 'Import Loaded'),
        ('export_empty', 'Export Empty'),
        ('import_empty', 'Import Empty'),
    )
    operation_type = models.CharField(max_length=15, choices=OPERATION_CHOICES, default='')

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    work_id = models.CharField(max_length=15, blank=True, default='')
    work_number = models.IntegerField(default=1)

    pickup_date = models.DateField(blank=True, null=True, default='')
    return_date = models.DateField(blank=True, null=True, default='')

    STATUS_CHOICES = (
        ('4', 'Return'),
        ('3', 'Pickup'),
        ('2', 'Completed'),
        ('1', '-'),
        ('0', 'Cancel'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=1)

    SUMMARY_STATUS_CHOICES = (
        ('1', 'Done'),
        ('0', '-'),
    )
    summary_status = models.CharField(max_length=1, choices=SUMMARY_STATUS_CHOICES, blank=True, null=True)

    detail = JSONField(null=True, blank=True)

    def __str__(self) :
        return self.work_id