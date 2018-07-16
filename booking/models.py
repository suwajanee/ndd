from django.db import models
from datetime import datetime

# Create your models here.
class Booking(models.Model):
    time = models.CharField(max_length=50, blank=True, default='')
    date = models.DateField(default=datetime.now)
    principal = models.CharField(max_length=50, blank=True)
    shipper = models.CharField(max_length=50, blank=True)
    agent = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    booking_no = models.CharField(max_length=50, blank=True)
    booking_color = models.CharField(max_length=20, blank=True, default='')
    fw_tr = models.CharField(max_length=50, blank=True)
    fw_fm = models.CharField(max_length=50, blank=True)
    container_no = models.CharField(max_length=50, blank=True)
    seal_no = models.CharField(max_length=50, blank=True)
    bw_tr = models.CharField(max_length=50, blank=True)
    bw_to = models.CharField(max_length=50, blank=True)
    vessel = models.CharField(max_length=50, blank=True)
    port = models.CharField(max_length=50, blank=True)
    closing_time = models.CharField(max_length=50, blank=True)
    remark = models.CharField(max_length=200, blank=True)
    loading = models.CharField(max_length=50, blank=True)
    work_id = models.CharField(max_length=50, blank=True)
    pickup_date = models.DateField( blank=True)
    factory_date = models.DateField(blank=True)
    return_date = models.DateField(blank=True)

    pickup_in_time = models.CharField(max_length=20, blank=True, default='')
    pickup_out_time = models.CharField(max_length=20, blank=True, default='')
    factory_in_time = models.CharField(max_length=20, blank=True, default='')
    factory_load_start_time = models.CharField(max_length=20, blank=True, default='')
    factory_load_finish_time = models.CharField(max_length=20, blank=True, default='')
    factory_out_finish = models.CharField(max_length=20, blank=True, default='')
    return_in_time = models.CharField(max_length=20, blank=True, default='')
    return_out_time = models.CharField(max_length=20, blank=True, default='')

    TEMPLATE_CHOICES = (
        ('full', 'Full'),
        ('forward', 'Forward'),
        ('backward', 'Backward'),
    )
    template_pdf = models.CharField(max_length=10, choices=TEMPLATE_CHOICES, default='full')

    ADDRESS_CHOICES = (
        ('shipper', 'Shipper'),
        ('other', 'Other'),
        ('none', 'None'),
    )
    address = models.CharField(max_length=10, choices=ADDRESS_CHOICES, default='shipper')
    address_other = models.CharField(max_length=500, blank=True, default='')

    def __str__(self) :
        return self.work_id