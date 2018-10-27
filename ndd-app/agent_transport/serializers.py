from rest_framework import serializers

from .models import AgentTransport
from customer.serializers import PrincipalSerializer, ShipperSerializer


class AgentTransportSerializer(serializers.ModelSerializer):
        shipper = ShipperSerializer()
        principal = PrincipalSerializer()
        class Meta:
                model = AgentTransport
                fields = '__all__'