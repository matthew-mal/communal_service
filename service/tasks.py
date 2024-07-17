from celery import shared_task
from .models import House, Tariff, Rent
from django.db import transaction
from datetime import date, timedelta


@shared_task
def calculate_rent(house_id, year, month):
    house = House.objects.get(id=house_id)
    water_tariff = Tariff.objects.get(name='Water')
    maintenance_tariff = Tariff.objects.get(name='Maintenance')
    start_date = date(year, month, 1)
    end_date = (start_date + timedelta(days=32)).replace(day=1)

    for apartment in house.apartments.all():
        total_water_cost = 0
        total_maintenance_cost = maintenance_tariff.price_per_unit * apartment.area

        for meter in apartment.water_meters.all():
            readings = meter.readings.filter(reading_date__range=[start_date, end_date]).order_by('reading_date')
            if readings.count() >= 2:
                water_usage = readings.last().value - readings.first().value
                total_water_cost += water_tariff.price_per_unit * water_usage

        total_rent = total_water_cost + total_maintenance_cost

        # Запись результатов в БД
        with transaction.atomic():
            Rent.objects.create(
                apartment=apartment,
                year=year,
                month=month,
                total_rent=total_rent
            )

    return f'Rent calculation for house {house_id} completed for {month}/{year}'
