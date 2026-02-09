from ..models import Trip, Driver, Transport, Client

class TripService:
    @staticmethod
    def trip_create(data: dict, driver: Driver, transport: Transport, client: Client):
        data["driver_id"] = driver
        data["transport_id"] = transport
        data["client_id"] = client
        trip = Trip.objects.create(**data)
        if trip.status == 'P':
            driver.status = 'OW'
            transport.status = "OW"
        
        if trip.status == 'C':
            driver.status = 'F'
            transport.status = 'F'
        
        transport.save()
        driver.save()

        return trip
    
    @staticmethod
    def trip_update(data: dict, trip: Trip, driver: Driver, transport: Transport, client: Client):
        data["driver_id"] = driver
        data["transport_id"] = transport
        data["client_id"] = client
        if trip.status == 'P':
            driver.status = 'OW'
            transport.status = "OW"
        
        if trip.status == 'C':
            driver.status = 'F'
            transport.status = 'F'

        transport.save()
        driver.save()

        trip.driver_id = driver
        trip.transport_id = transport
        trip.start_point = data.get("start_point", trip.start_point)
        trip.end_point = data.get("end_point", trip.end_point)
        trip.distance = data.get("distance", trip.distance)
        trip.fuel_status = data.get("fuel_status", trip.fuel_status)
        trip.fuel_actual = data.get("fuel_actual", trip.fuel_actual)
        trip.fuel_planned = data.get("fuel_planned", trip.fuel_planned)

        trip.save()

        return trip
        