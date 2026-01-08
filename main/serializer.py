from rest_framework import serializers
from .models import *

class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['id','transport_model', 'license_plate', 'fuel_rate', 'vin', 'mileage', 'status', 'to', 'miles_to_inspect', 'next_inspect']

        def validate(self, data):
            if data["mileage"] < 0:
                raise ValueError('Пробіг не може бути менше нуля')
            return data

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone', 'license', 'ipn', 'experience', 'status']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_type', 'first_name', 'last_name', 'phone', 'email', 'ipn', 'company_name', 'erdpou', 'created']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'driver_id', 'transport_id', 'client_id', 'start_point', 'end_point', 'status', 'distance', 'fuel_status', 'fuel_actual', 'fuel_planned']

class FuelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelLog
        fields = ['id', 'transport_id', 'trip_id', 'liters', 'price', 'timestamp']

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id', 'transport_id', 'type', 'cost', 'date']