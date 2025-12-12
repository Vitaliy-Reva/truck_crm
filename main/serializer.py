from rest_framework import serializers
from .models import *

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['id','transport_model', 'license_plate', 'fuel_rate', 'vin', 'mileage', 'status', 'to', 'miles_to_inspect', 'next_inspect']

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'license', 'itn', 'experience', 'phone', 'status']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'driver_id', 'transport_id', 'start_point', 'end_point', 'status', 'distance', 'fuel_status', 'fuel_actual', 'fuel_planned']

class FuelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelLog
        fields = ['id', 'transport_id', 'trip_id', 'liters', 'price', 'timestamp']

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id', 'transport_id', 'type', 'cost', 'date']