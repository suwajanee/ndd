from rest_framework import serializers

from .models import Year, FormDetail, CustomerCustom, SummaryWeek
from customer.serializers import PrincipalSerializer, ShipperSerializer


class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = '__all__'


class FormDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormDetail
        fields = '__all__'


class CustomerSettingSerializer(serializers.ModelSerializer):
    customer = PrincipalSerializer()
    form = FormDetailSerializer()
    class Meta:
        model = CustomerCustom
        fields = '__all__'


class SummaryWeekSerializer(serializers.ModelSerializer):
    year = YearSerializer()
    class Meta:
        model = SummaryWeek
        fields = '__all__'