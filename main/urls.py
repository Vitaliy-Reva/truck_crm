from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('transport/', transport_list, name='transport-list'),
    path('transport/<int:pk>/', transport_detail, name='transport-detail'),
    path('driver/', driver_list, name='driver-list'),
    path('driver/<int:pk>/', driver_detail, name='driver-detail'),
    path('client/', client_list, name='client-list'),
    path('client/<int:pk>', client_detail, name='client-detail'),
    path('order/', order_list, name='order-list'),
    path('order/<int:pk>/', order_detail, name='order-detail'),
    path('trip/', trip_list, name='trip-list'),
    path('trip/<int:pk>/', trip_detail, name='trip-detail'),
    path('fuel/', fuel_list, name='fuel-list'),
    path('fuel/<int:pk>/', fuel_detail, name='fuel-detail'),
    path('maintenance/', maintenance_list, name='maintenance-list'),
    path('maintenance/<int:pk>/', maintenance_detail, name='maintenance-detail'),
    path('client/', client_list, name='client-list'),
    path('client/<int:pk>/', client_detail, name='client_detail'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )