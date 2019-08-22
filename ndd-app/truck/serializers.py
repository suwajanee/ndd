from rest_framework import serializers

from .models import TruckManufacturer
from .models import Truck
from .models import Chassis


class TruckManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TruckManufacturer
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'


class ChassisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chassis
        fields = '__all__'
