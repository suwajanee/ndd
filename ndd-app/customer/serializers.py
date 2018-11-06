from rest_framework import serializers

from .models import Principal, Shipper, ShipperAddress


class PrincipalSerializer(serializers.ModelSerializer):   
        class Meta:
                model = Principal
                fields = '__all__'

class ShipperSerializer(serializers.ModelSerializer):
        class Meta:
                model = Shipper
                fields = '__all__'

class ShipperAddressSerializer(serializers.ModelSerializer):
        shipper = ShipperSerializer()
        class Meta:
                model = ShipperAddress
                fields = '__all__'