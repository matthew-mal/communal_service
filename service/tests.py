import datetime

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import House, Apartment, Tariff, WaterMeter, WaterMeterReading


class HouseViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.house = House.objects.create(street='test_street', number=1)

    def test_get_house_list(self):
        url = reverse('houses-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_house(self):
        url = reverse('houses-detail', kwargs={'pk': self.house.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['street'], 'test_street')

    def test_update_house(self):
        url = reverse('houses-detail', kwargs={'pk': self.house.pk})
        data = {
            'street': 'updated_street',
            'number': 2,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['street'], 'updated_street')
        self.assertEqual(response.data['number'], 2)

    def test_delete_house(self):
        url = reverse('houses-detail', kwargs={'pk': self.house.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(House.objects.count(), 0)

    def test_create_house(self):
        url = reverse('houses-list')
        data = {
            'street': 'new_street',
            'number': 3,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(House.objects.count(), 2)

    def test_create_house_invalid_data(self):
        url = reverse('houses-list')
        data = {
            'street': '',
            'number': 3,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(House.objects.count(), 1)

    def test_filter_house_by_number(self):
        url = reverse('houses-list')
        response = self.client.get(url, {'number': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['street'], 'test_street')


class ApartmentViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.house = House.objects.create(street='test_street', number=1)
        self.apartment = Apartment.objects.create(number='101', house=self.house, area=101)

    def test_get_apartment_list(self):
        url = reverse('apartments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_apartment(self):
        url = reverse('apartments-detail', kwargs={'pk': self.apartment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], 101)

    def test_update_apartment(self):
        url = reverse('apartments-detail', kwargs={'pk': self.apartment.pk})
        data = {
            'number': 102,
            'area': 102,
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['number'], 102)
        self.assertEqual(response.data['area'], 102)

    def test_delete_apartment(self):
        url = reverse('apartments-detail', kwargs={'pk': self.apartment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Apartment.objects.count(), 0)

    def test_create_apartment(self):
        url = reverse('apartments-list')
        data = {
            'number': '201',
            'area': 201,
            'house': self.house.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Apartment.objects.count(), 2)

    def test_create_apartment_invalid_data(self):
        url = reverse('apartments-list')
        data = {
            'number': '',
            'area': 301,
            'house': self.house.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Apartment.objects.count(), 1)

    def test_filter_apartment_by_house(self):
        url = reverse('apartments-list')
        response = self.client.get(url, {'house': self.house.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['number'], 101)


class TariffViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tariff = Tariff.objects.create(name='Test Tariff', price_per_unit=10.0)

    def test_get_tariff_list(self):
        url = reverse('tariffs-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_tariff(self):
        url = reverse('tariffs-detail', kwargs={'pk': self.tariff.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Tariff')

    def test_create_tariff(self):
        url = reverse('tariffs-list')
        data = {
            'name': 'New Tariff',
            'price_per_unit': 15.0,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tariff.objects.count(), 2)

    def test_update_tariff(self):
        url = reverse('tariffs-detail', kwargs={'pk': self.tariff.pk})
        data = {
            'name': 'Updated Tariff',
            'price_per_unit': 12.0,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Tariff')
        self.assertEqual(response.data['price_per_unit'], 12.0)

    def test_delete_tariff(self):
        url = reverse('tariffs-detail', kwargs={'pk': self.tariff.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tariff.objects.count(), 0)


class WaterMeterViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.house = House.objects.create(street='test_street', number=1)
        self.apartment = Apartment.objects.create(
            number='101',
            house=self.house,
            area=100
        )
        self.water_meter = WaterMeter.objects.create(
            serial_number='12345',
            apartment_id=self.apartment.id,
            installation_date=datetime.datetime.today()
        )

    def test_get_water_meter_list(self):
        url = reverse('water_meters-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_water_meter(self):
        url = reverse('water_meters-detail', kwargs={'pk': self.water_meter.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['serial_number'], '12345')

    def test_update_water_meter(self):
        url = reverse('water_meters-detail', kwargs={'pk': self.water_meter.pk})
        data = {
            'serial_number': '54321',
            'apartment': self.apartment.id,
            'installation_date': '2024-07-15'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['serial_number'], '54321')

    def test_delete_water_meter(self):
        url = reverse('water_meters-detail', kwargs={'pk': self.water_meter.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WaterMeter.objects.count(), 0)


class WaterMeterReadingViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.house = House.objects.create(street='test_street', number=1)
        self.apartment = Apartment.objects.create(
            number='101',
            house=self.house,
            area=100
        )
        self.water_meter = WaterMeter.objects.create(
            serial_number='12345',
            apartment_id=self.apartment.id,
            installation_date=datetime.datetime.today()
        )
        self.reading = WaterMeterReading.objects.create(
            water_meter_id=self.water_meter.id,
            value=100,
            reading_date=datetime.datetime.today()
        )

    def test_get_water_meter_reading_list(self):
        url = reverse('water_meter_readings-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_water_meter_reading(self):
        url = reverse('water_meter_readings-detail', kwargs={'pk': self.reading.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 100)

    def test_delete_water_meter_reading(self):
        url = reverse('water_meter_readings-detail', kwargs={'pk': self.reading.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WaterMeterReading.objects.count(), 0)
