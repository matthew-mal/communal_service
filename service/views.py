from celery.result import AsyncResult
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import House, Apartment, Tariff, WaterMeter, WaterMeterReading
from .serializers import HouseSerializer, ApartmentSerializer, TariffSerializer, WaterMeterSerializer, \
    WaterMeterReadingSerializer
from .tasks import calculate_rent


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class TariffViewSet(viewsets.ModelViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class WaterMeterViewSet(viewsets.ModelViewSet):
    queryset = WaterMeter.objects.all()
    serializer_class = WaterMeterSerializer


class WaterMeterReadingViewSet(viewsets.ModelViewSet):
    queryset = WaterMeterReading.objects.all()
    serializer_class = WaterMeterReadingSerializer


class CalculateRentView(APIView):
    def post(self, request, house_id, year, month):
        task = calculate_rent.delay(house_id, year, month)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)


class CheckCalculationProgressView(APIView):
    def get(self, request, task_id):
        task_result = AsyncResult(task_id)
        if task_result.state == 'SUCCESS':
            return Response({'status': task_result.state, 'result': task_result.result})
        else:
            return Response({'status': task_result.state})
