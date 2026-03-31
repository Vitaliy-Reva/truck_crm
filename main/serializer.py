from rest_framework import serializers
from django.http import JsonResponse
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
        fields = ['id', 'first_name', 'last_name', 'phone', 'photo', 'license', 'ipn', 'experience', 'status', 'weekend_until']


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
        fields = ['id', 'client_id', 'pay_id', 'order_name', 'price', 'status', 'address', 'payment_status', 'date']


class TripSerializer(PositiveValuesValidate, serializers.ModelSerializer):
    
    def validate_driver_id(self, driver):
        if self.instance is None:
            if driver.status == 'OW':
                raise serializers.ValidationError("Водій в поїздці. Назначте іншого водія")
            return driver
        
        if (self.instance.status == 'AC' and driver.status == 'OW') and driver.id != self.instance.driver_id.id:
            raise serializers.ValidationError("Водій в поїздці. Назначте іншого водія")
        
        if (self.instance.status in ('P', 'C')) and driver.id != self.instance.driver_id.id:
            raise serializers.ValidationError("Не можливо змінити водія під час поїздки")

        return driver

    def validate_transport_id(self, transport):
        if self.instance is None:
            if transport.status == 'OW':
                raise serializers.ValidationError("Транспорт в дорозі. Назначте інший транспорт")

            if transport.to == 'NS':
                raise serializers.ValidationError("Транспорт потребує ТО/Ремонту")
            elif transport.to in ('OS', 'R'):
                raise serializers.ValidationError("Транспорт на ТО/Ремонті")

            return transport
        
        if (self.instance.status == 'AC' and transport.status == 'OW') and transport.id != self.instance.transport_id.id:
            raise serializers.ValidationError("Транспорт в дорозі. Назначте інший транспорт")
        
        if (self.instance.status in ('P', 'C')) and transport.id != self.instance.transport_id.id:
            raise serializers.ValidationError("Не можливо змінити транспорт під час поїздки")

        if transport.to in ('NS', 'OS', 'R'):
            raise serializers.ValidationError("Транспорт потребує ТО/Ремонту або вже знаходиться на ТО/Ремонті")

        return transport
    
    def validate_order_id(self, order):
        if self.instance is None:
            if order.status == 'D':
                raise serializers.ValidationError("Замовлення вже доставляється")
            if order.status == 'E':
                raise serializers.ValidationError("Замовлення вже виконане")
            return order
        
        if (self.instance.status == 'AC' and order.status == 'D') and self.instance.order_id.id != order.id:
            raise serializers.ValidationError("Замовлення вже доставляється")
        
        if (self.instance.status in ('P', 'C')) and order.id != self.instance.order_id.id:
            raise serializers.ValidationError("Не можливо змінити замовлення під час поїздки")
        
        if order.status == 'E':
            raise serializers.ValidationError("Замовлення вже виконане")
        
        return order
    
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