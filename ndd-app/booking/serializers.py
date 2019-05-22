from rest_framework import serializers

from .models import Booking, BookingTime, ContainerSize
from customer.serializers import PrincipalSerializer, ShipperSerializer


class BookingSerializer(serializers.ModelSerializer):
        shipper = ShipperSerializer()
        principal = PrincipalSerializer()
        class Meta:
                model = Booking
                fields = '__all__'


class BookingTimeSerializer(serializers.ModelSerializer):
        booking = BookingSerializer()
        class Meta:
                model = BookingTime
                fields = '__all__'


class ContainerSizeSerializer(serializers.ModelSerializer):
        class Meta:
                model = ContainerSize
                fields = '__all__'