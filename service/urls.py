from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import HouseViewSet, ApartmentViewSet, TariffViewSet, WaterMeterViewSet, WaterMeterReadingViewSet

router = DefaultRouter()
router.register(r'houses', HouseViewSet)
router.register(r'apartments', ApartmentViewSet)
router.register(r'tariffs', TariffViewSet)
router.register(r'water_meters', WaterMeterViewSet)
router.register(r'water_meter_readings', WaterMeterReadingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('calculate_rent/<int:house_id>/<int:year>/<int:month>/', CalculateRentView.as_view(), name='calculate_rent'),
    path('calculation_progress/<str:task_id>/', CheckCalculationProgressView.as_view(), name='calculation_progress'),
]
