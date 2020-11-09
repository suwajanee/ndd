from django.contrib.postgres.fields import JSONField
from django.db import models

from agent_transport.models import AgentTransport
from booking.models import Booking
from employee.models import Driver
from summary.models import Year
from truck.models import Truck


class WorkOrder(models.Model):
    clear_date = models.DateField(blank=True, null=True, default=None)
    work_date = models.DateField(blank=True, null=True, default=None)

    work_normal = models.ForeignKey(Booking, on_delete=models.SET_NULL, blank=True, null=True)
    work_agent_transport = models.ForeignKey(AgentTransport, on_delete=models.SET_NULL, blank=True, null=True)
    order_type = models.CharField(max_length=5, blank=True, null=True)
    double_container = models.BooleanField(default=False)

    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, blank=True, null=True)

    detail = JSONField(blank=True, null=True, default=dict)
    price = JSONField(blank=True, null=True, default=dict)

    def work(self):
        if self.work_normal:
            return self.work_normal
        elif self.work_agent_transport:
            return self.work_agent_transport
        else:
            return

    def __str__(self):
        if self.order_type:
            order_type = ' / ' + self.order_type
            if self.double_container:
                order_type += ' +'
        else:
            order_type = ''

        if self.work_normal:
            return self.work_normal.work_id + order_type
        elif self.work_agent_transport:
            return self.work_agent_transport.work_id + order_type
        else:
            return str(self.pk)


class Expense(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, blank=True, null=True)
    co_expense = JSONField(blank=True, null=True, default=dict)
    cus_expense = JSONField(blank=True, null=True, default=dict)

    co_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cus_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        if self.work_order.work_normal:
            return self.work_order.work_normal.work_id
        elif self.work_order.work_agent_transport:
            return self.work_order.work_agent_transport.work_id
        else:
            return str(self.pk)


class ExpenseSummaryDate(models.Model):
    date = models.DateField(blank=True, null=True, default=None)
    month = models.CharField(max_length=2, blank=True, null=True)
    year = models.ForeignKey(Year, on_delete=models.SET_NULL, blank=True, null=True)
    co = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        if self.year:
            return str(self.date) + ' / ' + self.month + '/' + self.year.year_label + ' (' + self.co + ')'
        else:
            return str(self.date) + ' / ' + self.month + '/' + ' (' + self.co + ')'


class Variable(models.Model):
    key = models.CharField(max_length=10, blank=True, null=True)
    value = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.key

