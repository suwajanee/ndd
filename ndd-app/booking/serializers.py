from rest_framework import serializers

from .models import Booking
from customer.serializers import PrincipalSerializer, ShipperSerializer


class BookingSerializer(serializers.ModelSerializer):
        shipper = ShipperSerializer()
        principal = PrincipalSerializer()
        class Meta:
                model = Booking
                fields = '__all__'