from rest_framework import serializers

from .models import WorkOrder
from .models import Expense
from .models import ExpenseSummaryDate
from .models import Variable
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


class ExpenseThcSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer()
    total_expense = serializers.SerializerMethodField()

    try:
        thc_rate = Variable.objects.get(key='thc').value
        thc_rate = int(thc_rate)
    except Variable.DoesNotExist:
        thc_int = 0
    
    def get_total_expense(self, obj, thc_rate=thc_rate):
        if 'co_thc' in obj.co_expense:
            obj.total_expense['thc_rate'] = thc_rate
            obj.total_expense['company'] = obj.total_expense['company'] - eval(obj.co_expense['co_thc']) + thc_rate
            return obj.total_expense
        return obj.total_expense
    
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSummaryDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSummaryDate
        fields = '__all__'
