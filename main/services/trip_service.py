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
            order.status = 'D'
        
        if trip.status == 'C':
            driver.status = 'F'
            transport.status = 'F'
            order.status = 'E'
        
        trip.fuel_actual = transport.fuel_rate
        
        driver.save()
        transport.save()
        order.save()

        return trip
    
    @staticmethod
    def trip_update(data: dict, trip: Trip, driver: Driver, transport: Transport, client: Client, order: Order):

        data["end_point"] = order.address

        for key, value in data.items():
            if hasattr(trip, key) and key not in ['driver_id', 'transport_id', 'client_id', 'order_id']:
                setattr(trip, key, value)

        trip.driver_id = driver
        trip.transport_id = transport
        trip.client_id = client
        trip.order_id = order

        if not data.get('end_point'):
            trip.end_point = order.address

        new_status = data.get('status', trip.status)

        if new_status == 'P':
            driver.status = 'OW'
            transport.status = "OW"
            order.status = 'D'
        
        if new_status == 'C':
            driver.status = 'F'
            transport.status = 'F'
            order.status = 'E'

        # trip.fuel_actual = transport.fuel_rate

        driver.save()
        transport.save()
        order.save()
        trip.save()

        return trip
        