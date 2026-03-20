from rest_framework import serializers
from types import NoneType
from .models import *

class PositiveValuesValidate:
    def validate(self, attrs):
        for value in attrs.values():
            if isinstance(value, (int, float)):
                if value < 0:
                    raise serializers.ValidationError({"error": "Значення не може бути меншим за 0"})
        return attrs


class TransportSerializer(PositiveValuesValidate, serializers.ModelSerializer):
    def validate(self, attrs):

        if self.instance is None:
            return attrs

        new_mileage = attrs.get('mileage')
        old_mileage = self.instance.mileage

        if new_mileage is not None and new_mileage < 0:
            raise serializers.ValidationError({"mileage": 'Пробіг не може бути меншим за нуль'})
        
        if new_mileage < old_mileage:
            raise serializers.ValidationError({"mileage": 'Новий пробіг не може бути меншим за попередній'})

        return attrs        
    
    class Meta:
        model = Transport
        fields = ['id', 'transport_model', 'license_plate', 'fuel_rate', 'vin', 'mileage', 'photo', 'status', 'to', 'miles_to_inspect', 'next_inspect']


class DriverSerializer(PositiveValuesValidate, serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'phone', 'photo', 'license', 'ipn', 'experience', 'status']


class ClientSerializer(PositiveValuesValidate, serializers.ModelSerializer):

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        type = attrs.get("client_type")
        ipn = attrs.get("ipn")
        erdpou = attrs.get("erdpou")
        
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
        fields = ['pay_id', 'date', 'company', 'name', 'ipn', 'edrpou', 'total']


class OrderSerializer(PositiveValuesValidate, serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'client_id', 'pay_id', 'order_name', 'price', 'address', 'payment_status', 'date']


class TripSerializer(PositiveValuesValidate, serializers.ModelSerializer):

    def validate(self, attrs):
# Driver validation
        if self.instance is None:
            return attrs
        
        driver = attrs.get('driver_id')
        trip_status = self.instance.status
        print(trip_status)
        print(driver.status)

        if self.instance.driver_id == driver:
            return attrs

        if (trip_status == 'AC' and driver.status == 'OW') or (self.instance.driver_id.status == 'OW' and trip_status == 'P'):
            raise serializers.ValidationError({"driver": "Неможливо переназначити водія, поки поточний виконує поїздку"})

#Transport validation

        transport = attrs.get('transport_id')

        if self.instance.transport_id == transport:
            return attrs

        if transport.to == 'NS' or 'OS' or 'R':
            raise serializers.ValidationError({"transport": "Транспорт потребує ТО/Ремонту або вже знаходиться на ТО/Ремонті"})
        
        if transport.status == 'OW':
            raise serializers.ValidationError({"transport": "Транспорт в дорозі"})

        return attrs
    
    class Meta:
        model = Trip
        fields = ['id', 'driver_id', 'transport_id', 'client_id', 'order_id', 'start_point', 'end_point', 'status', 'distance', 'fuel_status', 'fuel_actual', 'fuel_planned']


class FuelLogSerializer(PositiveValuesValidate, serializers.ModelSerializer):
    
    class Meta:
        model = FuelLog
        fields = ['id', 'transport_id', 'trip_id', 'liters', 'price', 'timestamp']


class MaintenanceSerializer(PositiveValuesValidate, serializers.ModelSerializer):
    
    class Meta:
        model = Maintenance
        fields = ['id', 'transport_id', 'type', 'cost', 'date']