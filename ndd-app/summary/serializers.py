from rest_framework import serializers

from .models import Year
from customer.serializers import PrincipalSerializer, ShipperSerializer


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'