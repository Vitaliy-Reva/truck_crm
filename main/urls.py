from django.urls import path
from .views import transport_list, transport_detail

urlpatterns = [
    path('transport/', transport_list, name='transport-list'),
    path('transport/<int:pk>/', transport_detail, name='transport-detail'),
]