from django.contrib.postgres.fields import ArrayField
from django.db import models

from agent_transport.models import AgentTransport
from booking.models import Booking
from customer.models import Principal

# Create your models here.

class Year(models.Model):
    name = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.name


class FormDetail(models.Model):
    form_name = models.CharField(max_length=50, null=True, blank=True)
    form_detail = ArrayField(
        models.CharField(max_length=15, null=True, blank=True),
        size=4,
    )

    def __str__(self):
        return self.form_name


class CustomerForm(models.Model):
    customer = models.ForeignKey(Principal, on_delete=models.CASCADE, related_name="customerforms")
    sub_customer = models.CharField(max_length=50, null=True, blank=True)
    customer_title = models.CharField(max_length=50, null=True, blank=True)

    form = models.ForeignKey(FormDetail, on_delete=models.SET_NULL, null=True, blank=True)
    optional = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        if self.sub_customer:
            return self.sub_customer + '-' + self.customer.name
        return self.customer.name


STATUS_CHOICES = (
    ('0', '-'),
    ('1', 'Processing'),
    ('2', 'Finished'),
)
class SummaryWeek(models.Model):
    week = models.CharField(max_length=2, null=True, blank=True)
    month = models.CharField(max_length=2, null=True, blank=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, null=True, blank=True)
    
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    diesel_rate_of_week = models.CharField(max_length=5, null=True, blank=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.year.name + " - WK. " + self.week


class SummaryCustomer(models.Model):
    customer = models.ForeignKey(CustomerForm, on_delete=models.SET_NULL, null=True, blank=True)
    week = models.ForeignKey(SummaryWeek, on_delete=models.SET_NULL, null=True, blank=True)

    date_billing = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.week.year.name + " - WK. " + self.week.week + " - " + self.customer.customer.name


class Invoice(models.Model):
    invoice_no = models.CharField(max_length=15, null=True, blank=True)
    customer_week = models.ForeignKey(SummaryCustomer, on_delete=models.SET_NULL, null=True, blank=True)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return self.invoice_no


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)

    work_normal = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True, blank=True)
    work_agent_transport = models.ForeignKey(AgentTransport, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def work(self):
        if not self.invoice:
            return
        elif self.invoice.customer_week.customer.customer.work_type == 'normal' :
            return self.work_normal
        elif self.invoice.customer_week.customer.customer.work_type == 'agent-transport' :
            return self.work_agent_transport

    def __str__(self):
        if not self.invoice:
            return str(self.pk)
        return self.invoice.invoice_no
