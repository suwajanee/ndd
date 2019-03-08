from rest_framework import serializers

from .models import Booking, BookingTime
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