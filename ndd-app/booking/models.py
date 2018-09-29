from django.db import models
from datetime import datetime
from customer.models import Principal, Shipper

# Create your models here.

class Booking(models.Model):
    time = models.CharField(max_length=50, blank=True, default='')
    date = models.DateField(default=datetime.now, null=True)
    principal = models.ForeignKey(Principal, on_delete=models.SET_NULL, null=True, blank=True)
    shipper = models.ForeignKey(Shipper, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    booking_no = models.CharField(max_length=50, blank=True)

    NDD_CHOICES = (
        ('1', 'Yes'),
        ('0', '-'),
    )
    start = models.CharField(max_length=20, blank=True, default='')
    pickup_tr = models.CharField(max_length=20, blank=True, default='')
    pickup_from = models.CharField(max_length=20, blank=True, default='')

    yard_ndd = models.CharField(max_length=1, choices=NDD_CHOICES, default=0)

    forward_tr = models.CharField(max_length=20, blank=True, default='')
    factory = models.CharField(max_length=20, blank=True, default='')
    backward_tr = models.CharField(max_length=20, blank=True, default='')

    fac_ndd = models.CharField(max_length=1, choices=NDD_CHOICES, default=0)

    return_tr = models.CharField(max_length=20, blank=True, default='')
    return_to = models.CharField(max_length=20, blank=True, default='')

    container_no = models.CharField(max_length=50, blank=True)
    seal_no = models.CharField(max_length=50, blank=True)
    vessel = models.CharField(max_length=50, blank=True)
    port = models.CharField(max_length=50, blank=True)
    closing_date = models.DateField(max_length=20, null=True, blank=True, default=None)
    closing_time = models.CharField(max_length=20, blank=True)
    ref = models.CharField(max_length=200, blank=True, default='')
    remark = models.CharField(max_length=200, blank=True)
    
    work_id = models.CharField(max_length=50, blank=True)
    work_number = models.IntegerField(default=1)

    pickup_date = models.DateField( blank=True, null=True)
    factory_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    pickup_in_time = models.CharField(max_length=50, blank=True, default='')
    pickup_out_time = models.CharField(max_length=50, blank=True, default='')
    factory_in_time = models.CharField(max_length=50, blank=True, default='')
    factory_load_start_time = models.CharField(max_length=50, blank=True, default='')
    factory_load_finish_time = models.CharField(max_length=50, blank=True, default='')
    factory_out_time = models.CharField(max_length=50, blank=True, default='')
    return_in_time = models.CharField(max_length=50, blank=True, default='')
    return_out_time = models.CharField(max_length=50, blank=True, default='')

    NEXTDAY_CHOICES = (
        ('1', 'Yes'),
        ('0', '-'),
    )
    nextday = models.CharField(max_length=1, choices=NEXTDAY_CHOICES, default=0)

    STATUS_CHOICES = (
        ('2', 'Finished'),
        ('1', '-'),
        ('0', 'Cancel'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    def __str__(self) :
        return self.work_id