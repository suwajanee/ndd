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
    full_order = serializers.SerializerMethodField()

    def get_full_order(self, obj):
        order = obj.order_type
        if obj.double_container:
            order += ' +'
        return order

    class Meta:
        model = WorkOrder
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer()
    
    class Meta:
        model = Expense
        fields = '__all__'

    
class ExpenseContainerSerializer(serializers.ModelSerializer):
    work_order = WorkOrderSerializer()
    work_detail = serializers.SerializerMethodField()

    def get_work_detail(self, obj):
        work_order = obj.work_order
        if work_order.work_normal:
            work_type = 'normal'
            work = work_order.work_normal
            size = work.size
            container = work.container_no

            if '2X' in size:
                container += '-' + work.seal_no
            elif 'container_2' in work_order.detail:
                size = '2X' + size
                container += '-' + work_order.detail['container_2']

        elif work_order.work_agent_transport:
            work_type = 'agent-transport'
            work = work_order.work_agent_transport
            size = work.size
            container = work.container_1

            if '2X' in size:
                container += '-' + work.container_2
        
        data = {
            'work_type': work_type,
            'size': size,
            'container': container,
            'booking_no': work.booking_no
        }
        return data

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
