from rest_framework import serializers

from .models import Year, FormDetail
from customer.serializers import PrincipalSerializer, ShipperSerializer


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class FormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDetail
        fields = '__all__'