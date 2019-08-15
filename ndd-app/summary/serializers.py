from rest_framework import serializers

from .models import Year, FormDetail, CustomerCustom, SummaryWeek, SummaryCustomer, Invoice, InvoiceDetail
from customer.serializers import PrincipalSerializer, ShipperSerializer
from agent_transport.serializers import AgentTransportSerializer
from booking.serializers import BookingSerializer


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class FormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDetail
        fields = '__all__'


class CustomerCustomSerializer(serializers.ModelSerializer):
    customer = PrincipalSerializer()
    form = FormDetailSerializer()
    class Meta:
        model = CustomerCustom
        fields = '__all__'


class SummaryWeekSerializer(serializers.ModelSerializer):
    year = YearSerializer()
    class Meta:
        model = SummaryWeek
        fields = '__all__'


class SummaryCustomerSerializer(serializers.ModelSerializer):
    customer_main = PrincipalSerializer()
    customer_custom = CustomerCustomSerializer()
    week = SummaryWeekSerializer()
    class Meta:
        model = SummaryCustomer
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    customer_week = SummaryCustomerSerializer()
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):
    work_normal = BookingSerializer()
    work_agent_transport = AgentTransportSerializer()
    class Meta:
        model = InvoiceDetail
        fields = '__all__'


class CommissionSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()
    work_normal = BookingSerializer()
    work_agent_transport = AgentTransportSerializer()
    class Meta:
        model = InvoiceDetail
        fields = '__all__'