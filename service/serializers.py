from rest_framework import serializers
from .models import House, Apartment, Tariff, WaterMeter, WaterMeterReading


class WaterMeterReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterMeterReading
        fields = ('water_meter', 'reading_date', 'value')


class WaterMeterSerializer(serializers.ModelSerializer):
    readings = WaterMeterReadingSerializer(many=True, read_only=True)

    class Meta:
        model = WaterMeter
        fields = ('apartment', 'installation_date', 'serial_number', 'readings')


class ApartmentSerializer(serializers.ModelSerializer):
    water_meters = WaterMeterSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = ('house', 'number', 'area', 'water_meters')


class HouseSerializer(serializers.ModelSerializer):
    apartments = ApartmentSerializer(many=True, read_only=True)

    class Meta:
        model = House
        fields = ('street', 'number', 'apartments')


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ('name', 'price_per_unit')
