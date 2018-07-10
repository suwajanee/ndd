from django.db import models
from datetime import datetime

# Create your models here.
class Booking(models.Model):
    time = models.TimeField(blank=True, null=True)
    date = models.DateField(default=datetime.now)
    principal = models.CharField(max_length=200, blank=True)
    shipper = models.CharField(max_length=200, blank=True)
    agent = models.CharField(max_length=200, blank=True)
    size = models.CharField(max_length=200, blank=True)
    booking_no = models.CharField(max_length=200, blank=True)
    fw_tr = models.CharField(max_length=200, blank=True)
    fw_fm = models.CharField(max_length=200, blank=True)
    container_no = models.CharField(max_length=200, blank=True)
    seal_no = models.CharField(max_length=200, blank=True)
    bw_tr = models.CharField(max_length=200, blank=True)
    bw_to = models.CharField(max_length=200, blank=True)
    vessel = models.CharField(max_length=200, blank=True)
    port = models.CharField(max_length=200, blank=True)
    closing_time = models.CharField(max_length=200, blank=True)
    remark = models.CharField(max_length=200, blank=True)
    loading = models.CharField(max_length=200, blank=True)
    work_id = models.CharField(max_length=200, blank=True)
    pickup_date = models.DateField( blank=True)
    factory_date = models.DateField(blank=True)
    return_date = models.DateField(blank=True)

    def __str__(self) :
        return self.work_id