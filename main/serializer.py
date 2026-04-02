from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from .errors import error_response
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
            exc = APIException(error_response('01_01'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        if new_mileage < old_mileage:
            exc = APIException(error_response('01_02'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc

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
            exc = APIException(error_response('03_01'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        elif type == 'FOP' and not ipn:
            exc = APIException(error_response('03_02'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        elif type == 'COMP' and not erdpou:
            exc = APIException(error_response('03_03'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        if type == 'COMP' and not first_name and not last_name:
            exc = APIException(error_response('03_04'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
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
                exc = APIException(error_response('06_01'))
                exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                raise exc
            return driver
        
        if (self.instance.status == 'AC' and driver.status == 'OW') and driver.id != self.instance.driver_id.id:
            exc = APIException(error_response('06_01'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        if (self.instance.status in ('P', 'C')) and driver.id != self.instance.driver_id.id:
            exc = APIException(error_response('06_02'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc

        return driver

    def validate_transport_id(self, transport):
        if self.instance is None:
            if transport.status == 'OW':
                exc = APIException(error_response('06_03'))
                exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                raise exc

            if transport.to == 'NS':
                exc = APIException(error_response('06_04'))
                exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                raise exc
            elif transport.to in ('OS', 'R'):
                exc = APIException(error_response('06_05'))
                exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                raise exc

            return transport
        
        if (self.instance.status == 'AC' and transport.status == 'OW') and transport.id != self.instance.transport_id.id:
            exc = APIException(error_response('06_03'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        if (self.instance.status in ('P', 'C')) and transport.id != self.instance.transport_id.id:
            exc = APIException(error_response('06_06'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc

        if transport.to == 'NS':
            exc = APIException(error_response('06_04'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        elif transport.to in ('OS', 'R'):
            exc = APIException(error_response('06_05'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc

        return transport
    
    def validate_order_id(self, order):
        if self.instance is None:
            if order.status == 'D':
                exc = APIException(error_response('06_07'))
                exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                raise exc
            if order.status == 'E':
                exc = APIException(error_response('06_08'))
                exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
                raise exc
            return order
        
        if (self.instance.status == 'AC' and order.status == 'D') and self.instance.order_id.id != order.id:
            exc = APIException(error_response('06_07'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        if (self.instance.status in ('P', 'C')) and order.id != self.instance.order_id.id:
            exc = APIException(error_response('06_09'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
        if order.status == 'E':
            exc = APIException(error_response('06_08'))
            exc.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            raise exc
        
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