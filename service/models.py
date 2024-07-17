from django.db import models


class House(models.Model):
    street = models.CharField(max_length=100)
    number = models.IntegerField()

    def __str__(self):
        return f'{self.street}, {self.number}'


class Apartment(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='apartments')
    number = models.SmallIntegerField()
    area = models.FloatField()  # площадь в квадратных метрах

    def __str__(self):
        return f"Apartment {self.number} in {self.house}"


class Tariff(models.Model):
    name = models.CharField(max_length=100)
    price_per_unit = models.FloatField()

    def __str__(self):
        return f"{self.name}: {self.price_per_unit} per unit"


class WaterMeter(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='watermeters')
    installation_date = models.DateField()
    serial_number = models.CharField(max_length=50)

    def __str__(self):
        return f"Water meter in {self.apartment}"


class WaterMeterReading(models.Model):
    water_meter = models.ForeignKey(WaterMeter, on_delete=models.CASCADE, related_name='readings')
    reading_date = models.DateField()
    value = models.FloatField()  # показания счетчика

    class Meta:
        unique_together = ('water_meter', 'reading_date')

    def __str__(self):
        return f"Reading on {self.reading_date} for {self.water_meter}: {self.value}"


class Rent(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='rents', on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_rent = models.FloatField()

    def __str__(self):
        return f"Rent for {self.apartment} for {self.month}/{self.year}: {self.total_rent}"