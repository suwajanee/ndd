from rest_framework import serializers

from .models import Driver
from .models import Employee
from .models import Job
from .models import Salary
from truck.serializers import TruckSerializer


class JobSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return Employee.objects.filter(status='a', job__job_title=obj.job_title).count()

    class Meta:
        model = Job
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.name_title + ' ' + obj.first_name + ' ' + obj.last_name

    class Meta:
        model = Employee
        fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    truck = TruckSerializer()
    class Meta:
        model = Driver
        fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = Salary
        fields = '__all__'
    