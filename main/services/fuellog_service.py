from ..models import FuelLog, Trip, Transport

class FuelLogService:
    @staticmethod
    def fuellog_create(data: dict, trip: Trip, transport: Transport):
        data["transport_id"] = transport
        data["trip_id"] = trip
        fuellog =  FuelLog.objects.create(**data)

        transport.fuel_rate += fuellog.liters
        trip.fuel_actual = transport.fuel_rate

        if trip.fuel_actual > trip.fuel_planned:
            trip.fuel_status = 'O'

        transport.save()
        trip.save()
        return fuellog
    
    @staticmethod
    def fuellog_update(data: dict, fuellog: FuelLog, trip: Trip, transport: Transport):
        data["transport_id"] = transport
        data["trip_id"] = trip

        transport.fuel_rate += fuellog.liters
        trip.fuel_actual = transport.fuel_rate

        if trip.fuel_actual > trip.fuel_planned:
            trip.fuel_status = 'O'
        
        trip.save()
        transport.save()
        fuellog.save()
        
        return fuellog