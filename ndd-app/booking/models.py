from django.contrib.postgres.fields import JSONField
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

    NDD_CHOICES_1 = (
        ('1', 'NDD'),
        ('0', '-'),
    )
    start = models.CharField(max_length=20, blank=True, default='')
    pickup_tr = models.CharField(max_length=20, blank=True, default='')
    pickup_from = models.CharField(max_length=20, blank=True, default='')

    yard_ndd = models.CharField(max_length=1, choices=NDD_CHOICES_1, default=0)

    forward_tr = models.CharField(max_length=20, blank=True, default='')
    factory = models.CharField(max_length=20, blank=True, default='')
    backward_tr = models.CharField(max_length=20, blank=True, default='')

    NDD_CHOICES_2 = (
        ('2', 'Fac'),
        ('1', 'NDD'),
        ('0', '-'),
    )
    fac_ndd = models.CharField(max_length=1, choices=NDD_CHOICES_2, default=0)

    return_tr = models.CharField(max_length=20, blank=True, default='')
    return_to = models.CharField(max_length=20, blank=True, default='')

    container_no = models.CharField(max_length=50, blank=True)
    seal_no = models.CharField(max_length=50, blank=True)
    tare = models.CharField(max_length=100, blank=True, default='')

    vessel = models.CharField(max_length=50, blank=True)
    port = models.CharField(max_length=50, blank=True)
    closing_date = models.DateField(max_length=20, null=True, blank=True, default=None)
    closing_time = models.CharField(max_length=20, blank=True)
    remark = models.CharField(max_length=200, blank=True)
    
    work_id = models.CharField(max_length=50, blank=True)
    work_number = models.IntegerField(default=1)

    pickup_date = models.DateField( blank=True, null=True)
    factory_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

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
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=1)

    SUMMARY_STATUS_CHOICES = (
        ('1', 'Done'),
        ('0', '-'),
    )
    summary_status = models.CharField(max_length=1, choices=SUMMARY_STATUS_CHOICES)

    def __str__(self) :
        return self.work_id


class BookingTime(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="bookingtimes")

    pickup_in_time = JSONField(null=True, blank=True)
    pickup_out_time = JSONField(null=True, blank=True)
    factory_in_time = JSONField(null=True, blank=True)
    factory_load_start_time = JSONField(null=True, blank=True)
    factory_load_finish_time = JSONField(null=True, blank=True)
    factory_out_time = JSONField(null=True, blank=True)
    return_in_time = JSONField(null=True, blank=True)
    return_out_time = JSONField(null=True, blank=True)