from django.urls import path
from .views import *

urlpatterns = [
    path('transport/', transport_list, name='transport-list'),
    path('transport/<int:pk>/', transport_detail, name='transport-detail'),
    path('driver/', driver_list, name='driver-list'),
    path('driver/<int:pk>/', driver_detail, name='driver-detail'),
    path('trip/', trip_list, name='trip-list'),
    path('trip/<int:pk>/', trip_detail, name='trip-detail'),
    path('fuel/', fuel_list, name='fuel-list'),
    path('fuel/<int:pk>/', fuel_detail, name='fuel-detail'),
    path('maintenance/', maintenance_list, name='maintenance-list'),
    path('maintenance/<int:pk>/', maintenance_detail, name='maintenance-detail'),
]