from django.db import models
from datetime import datetime
from customer.models import Principal, Shipper

# Create your models here.

class AgentTransport(models.Model):
    date = models.DateField(default=datetime.now, null=True)
    principal = models.ForeignKey(Principal, on_delete=models.SET_NULL, null=True, blank=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    booking_no = models.CharField(max_length=50, blank=True)

    pickup_tr = models.CharField(max_length=20, blank=True, default='')
    pickup_from = models.CharField(max_length=20, blank=True, default='')
    return_tr = models.CharField(max_length=20, blank=True, default='')
    return_to = models.CharField(max_length=20, blank=True, default='')

    container_1 = models.CharField(max_length=50, blank=True, default='')
    container_2 = models.CharField(max_length=50, blank=True, default='')
    ref = models.CharField(max_length=200, blank=True, default='')
    remark = models.CharField(max_length=200, blank=True, default='')
    
    WORK_CHOICES = (
        ('ep', 'Empty'),
        ('fc', 'Full'),
    )
    work_type = models.CharField(max_length=10, choices=WORK_CHOICES, default='ep')
    work_id = models.CharField(max_length=50, blank=True, default='')
    work_number = models.IntegerField(default=1)

    pickup_date = models.DateField(blank=True, null=True, default='')
    return_date = models.DateField(blank=True, null=True, default='')

    STATUS_CHOICES = (
        ('2', 'Finished'),
        ('1', '-'),
        ('0', 'Cancel'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=1)

    def __str__(self) :
        return self.work_id