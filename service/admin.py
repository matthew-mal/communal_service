from django.contrib import admin
from .models import House, Tariff, WaterMeter, WaterMeterReading, Apartment, Rent


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    pass


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('house', 'number', 'area')
    list_filter = ('house', 'area')


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_unit')


@admin.register(WaterMeter)
class WaterMeterAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'installation_date', 'serial_number')


@admin.register(WaterMeterReading)
class WaterMeterReadingAdmin(admin.ModelAdmin):
    list_display = ('water_meter', 'reading_date', 'value')


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'year', 'month', 'total_rent')
    list_filter = ('apartment', 'year', 'month')
