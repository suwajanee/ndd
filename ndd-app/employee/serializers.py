from rest_framework import serializers

from .models import Driver
from .models import Employee
from .models import Job
from .models import Salary


class JobSerializer(serializers.ModelSerializer):   
        class Meta:
                model = Job
                fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
        job = JobSerializer()
        class Meta:
                model = Employee
                fields = '__all__'


class DriverSerializer(serializers.ModelSerializer):
        employee = EmployeeSerializer()
        class Meta:
                model = Driver
                fields = '__all__'


class SalarySerializer(serializers.ModelSerializer):
        employee = EmployeeSerializer()
        class Meta:
                model = Salary
                fields = '__all__'
