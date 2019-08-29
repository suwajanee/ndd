from rest_framework import serializers

from .models import Manufacturer
from .models import Truck
from .models import Chassis


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    class Meta:
        model = Truck
        fields = '__all__'


class ChassisSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturerSerializer()
    class Meta:
        model = Chassis
        fields = '__all__'
