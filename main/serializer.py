from rest_framework import serializers
from .models import *

class TransportSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        new_mileage = attrs.get('mileage')

        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})

        if new_mileage is not None and new_mileage < 0:
            raise serializers.ValidationError({"mileage": 'Пробіг не може бути меншим за нуль'})
        
        if self.instance is not None:
            old_mileage = self.instance.mileage
            if new_mileage < old_mileage:
                raise serializers.ValidationError({"mileage": 'Новий пробіг не може бути меншим за попередній'})

        return attrs        
    
    class Meta:
        model = Transport
        fields = ['id', 'transport_model', 'license_plate', 'fuel_rate', 'vin', 'mileage', 'photo', 'status', 'to', 'miles_to_inspect', 'next_inspect']


class DriverSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        return attrs

    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone', 'photo', 'license', 'ipn', 'experience', 'status']

class ClientSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        type = attrs.get("client_type")
        ipn = attrs.get("ipn")
        erdpou = attrs.get("erdpou")

        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        
        if type == 'FIZ' and not ipn:
            raise serializers.ValidationError({"ipn": "Фізична особа обов'язково має мати ідентифікаційний код"})
        elif type == 'FOP' and not ipn:
            raise serializers.ValidationError({"ipn": "ФОП обов'язково має мати ідентифікаційний код"})
        elif type == 'COMP' and not erdpou:
            raise serializers.ValidationError({"erdpou": "Компанія обов'язково має мати ЄРДПОУ"})
        
        if type == 'COMP' and not first_name and not last_name:
            raise serializers.ValidationError({"first_name, last_name": "Компанія повинна мати представника"})
        
        return attrs

    class Meta:
        model = Client
        fields = ['id', 'client_type', 'first_name', 'last_name', 'phone', 'email', 'ipn', 'company_name', 'edrpou', 'created']
    
class NoPayedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoPayedOrder
        fields = ['id', 'date', 'company', 'name', 'ipn', 'edrpou', 'total']

class OrderSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        return attrs

    class Meta:
        model = Order
        fields = ['id', 'client_id', 'pay_id', 'order_name', 'price', 'address', 'payment_status', 'date']

class TripSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        return attrs
    
    class Meta:
        model = Trip
        fields = ['id', 'driver_id', 'transport_id', 'client_id', 'order_id', 'start_point', 'end_point', 'status', 'distance', 'fuel_status', 'fuel_actual', 'fuel_planned']

class FuelLogSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        return attrs
    
    class Meta:
        model = FuelLog
        fields = ['id', 'transport_id', 'trip_id', 'liters', 'price', 'timestamp']

class MaintenanceSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        return attrs
    
    class Meta:
        model = Maintenance
        fields = ['id', 'transport_id', 'type', 'cost', 'date']