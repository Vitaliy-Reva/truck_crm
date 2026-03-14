from ..models import Trip, Driver, Transport, Client, Order

class TripService:
    @staticmethod
    def trip_create(data: dict, driver: Driver, transport: Transport, client: Client, order: Order):
        data["driver_id"] = driver
        data["transport_id"] = transport
        data["client_id"] = client
        data["order_id"] = order

        data["end_point"] = order.address

        trip = Trip.objects.create(**data)
        if trip.status == 'P':
            driver.status = 'OW'
            transport.status = "OW"
        
        if trip.status == 'C':
            driver.status = 'F'
            transport.status = 'F'
        
        trip.fuel_actual = transport.fuel_rate
        
        transport.save()
        driver.save()

        return trip
    
    @staticmethod
    def trip_update(data: dict, trip: Trip, driver: Driver, transport: Transport, client: Client, order: Order):
        data["driver_id"] = driver
        data["transport_id"] = transport
        data["client_id"] = client

        data["end_point"] = order.address

        new_status = data.get('status', trip.status)

        if new_status == 'P':
            driver.status = 'OW'
            transport.status = "OW"
        
        if new_status == 'C':
            driver.status = 'F'
            transport.status = 'F'

        transport.save()
        driver.save()
        trip.save()

        return trip
        