from rest_framework import serializers

from .models import WorkOrder
from .models import Expense
from .models import ExpenseSummaryDate
from agent_transport.serializers import AgentTransportSerializer
from booking.serializers import BookingSerializer
from employee.serializers import DriverSerializer
from truck.serializers import TruckSerializer


class WorkOrderSerializer(serializers.ModelSerializer):
    work_normal = BookingSerializer()
    work_agent_transport = AgentTransportSerializer()
    driver = DriverSerializer()
    truck = TruckSerializer()
    work = BookingSerializer() or AgentTransportSerializer()
    class Meta:
        model = WorkOrder
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer()
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSummaryDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSummaryDate
        fields = '__all__'
