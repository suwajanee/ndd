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
    thc_rate = serializers.SerializerMethodField()
    co_total = serializers.SerializerMethodField()

    try:
        thc = Variable.objects.get(key='thc').value
        thc = int(thc)
    except Variable.DoesNotExist:
        thc = 0

    def get_co_total(self, obj, thc=thc):
        if 'co_thc' in obj.co_expense:
            return obj.co_total - eval(obj.co_expense['co_thc']) + thc
        return obj.co_total
    
    def get_thc_rate(self, obj, thc=thc):
        if 'co_thc' in obj.co_expense:
            return thc
    
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSummaryDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSummaryDate
        fields = '__all__'
