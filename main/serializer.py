from rest_framework import serializers
from .models import *

class TransportSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        new_mileage = attrs.get('mileage')

        if new_mileage is not None and new_mileage < 0:
            raise serializers.ValidationError({"mileage": 'Пробіг не може бути меншим за нуль'})
        
        if self.instance is not None:
            old_mileage = self.instance.mileage
            if new_mileage < old_mileage:
                raise serializers.ValidationError({"mileage": 'Новий пробіг не може бути меншим за попередній'})

        return attrs        
    
    class Meta:
        model = Transport
        fields = ['id', 'transport_model', 'license_plate', 'fuel_rate', 'vin', 'mileage', 'status', 'to', 'miles_to_inspect', 'next_inspect']


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone', 'license', 'ipn', 'experience', 'status']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'client_type', 'first_name', 'last_name', 'phone', 'email', 'ipn', 'company_name', 'erdpou', 'created']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'client_id', 'order_name', 'price', 'payment', 'date']

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