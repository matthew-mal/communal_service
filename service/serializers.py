from rest_framework import serializers
from .models import House, Apartment, Tariff, WaterMeter, WaterMeterReading, Rent


class WaterMeterReadingSerializer(serializers.ModelSerializer):
    water_meter_id = serializers.SerializerMethodField()

    class Meta:
        model = WaterMeterReading
        fields = ('water_meter_id', 'reading_date', 'value')

    def get_water_meter_id(self, obj):
        return obj.water_meter.id


class WaterMeterSerializer(serializers.ModelSerializer):
    readings = WaterMeterReadingSerializer(many=True, read_only=True)
    apartment_id = serializers.SerializerMethodField()

    class Meta:
        model = WaterMeter
        fields = ('apartment_id', 'installation_date', 'serial_number', 'readings')

    def get_apartment_id(self, obj):
        return obj.apartment.id


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


class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = ('apartment', 'year', 'month', 'total_rent')
