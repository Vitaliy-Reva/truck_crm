from ..models import Transport

class TransportService:
    @staticmethod
    def create_transport(data: dict):
        return Transport.objects.create(**data)
    
    @staticmethod
    def update_transport(data: dict, transport: Transport, new_mileage: int):
        print(data)
        if transport.mileage >= transport.next_inspect:
            transport.to = 'NS'
            transport.next_inspect += transport.miles_to_inspect
        
        transport.mileage = new_mileage
        
        transport.transport_model = data.get("transport_model", transport.transport_model)
        transport.license_plate = data.get("license_plate", transport.license_plate)
        transport.fuel_rate = data.get("fuel_rate", transport.fuel_rate)
        transport.vin = data.get("vin", transport.vin)
        transport.status = data.get('status', transport.status)
        transport.miles_to_inspect = data.get("miles_to_inspect", transport.miles_to_inspect)
        transport.next_inspect = data.get("next_inspect", transport.next_inspect)
        
        transport.save()
        return transport
