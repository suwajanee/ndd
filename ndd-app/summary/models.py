from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.db import models

from agent_transport.models import AgentTransport
from booking.models import Booking
from customer.models import Principal

# Create your models here.

class Year(models.Model):
    year_label = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.year_label


class FormDetail(models.Model):
    form_name = models.CharField(max_length=50, null=True, blank=True)
    form_detail = ArrayField(
        models.CharField(max_length=15, null=True, blank=True),
        size=10,
    )

    def __str__(self):
        return self.form_name


class CustomerCustom(models.Model):
    customer = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name="customercustoms")
    sub_customer = models.CharField(max_length=50, null=True, blank=True)
    customer_title = models.CharField(max_length=50, null=True, blank=True)

    form = models.ForeignKey(FormDetail, on_delete=models.SET_NULL, null=True, blank=True)
    option = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        if self.sub_customer:
            return self.sub_customer + '-' + self.customer.name
        return self.customer.name


STATUS_CHOICES = (
    ('0', 'Processing'),
    ('1', 'Finished'),
)
class SummaryWeek(models.Model):
    week = models.CharField(max_length=2, null=True, blank=True)
    month = models.CharField(max_length=2, null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True, blank=True)
    
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    diesel_rate = models.CharField(max_length=5, null=True, blank=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    def __str__(self):
        if self.year:
            return self.year.year_label + " - WK. " + self.week
        return "WK. " + self.week


class SummaryCustomer(models.Model):
    customer_main = models.ForeignKey(Principal, on_delete=models.SET_NULL, null=True, blank=True)
    customer_custom = models.ForeignKey(CustomerCustom, on_delete=models.SET_NULL, null=True, blank=True)

    week = models.ForeignKey(SummaryWeek, on_delete=models.SET_NULL, null=True, blank=True)

    date_billing = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    detail = models.CharField(max_length=100, null=True, blank=True, default='')

    @property
    def customer(self):
        if not self.customer_custom and not self.customer_main:
            return
        elif self.customer_custom:
            return self.customer_custom
        elif self.customer_main:
            return self.customer_main


    def __str__(self):
        if self.week and self.customer_custom:
            return self.week.year.year_label + " - WK. " + self.week.week + " - " + self.customer_main.name + " - " + self.customer_custom.sub_customer
        elif self.week and self.customer_main:
            return self.week.year.year_label + " - WK. " + self.week.week + " - " + self.customer_main.name
        else:
            return str(self.pk)
            

class Invoice(models.Model):
    invoice_no = models.CharField(max_length=25, null=True, blank=True)
    customer_week = models.ForeignKey(SummaryCustomer, on_delete=models.SET_NULL, null=True, blank=True)

    drayage_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    gate_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    detail = JSONField(null=True, blank=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return str(self.customer_week) + " - " + self.invoice_no


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)

    work_normal = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    work_agent_transport = models.ForeignKey(AgentTransport, on_delete=models.SET_NULL, null=True, blank=True)

    drayage_charge = JSONField(null=True, blank=True)
    gate_charge = JSONField(null=True, blank=True)

    detail = JSONField(null=True, blank=True)

    @property
    def work(self):
        if not self.invoice:
            return
        elif self.invoice.customer_week.customer_main.work_type == 'normal' :
            return self.work_normal
        elif self.invoice.customer_week.customer_main.work_type == 'agent-transport' :
            return self.work_agent_transport

    def __str__(self):
        if not self.invoice:
            return str(self.pk)
        return self.invoice.invoice_no
