from ..models import Transport

class TransportService:
    @staticmethod
    def create_transport(data: dict):
        transport = Transport.objects.create(**data)
        transport.next_inspect = transport.mileage + transport.miles_to_inspect
        transport.save()
        return transport
    
    @staticmethod
    def update_transport(transport: Transport, data: dict):

        new_mileage = data["mileage"]

        if new_mileage >= transport.next_inspect:
            transport.to = 'NS'
            transport.next_inspect += transport.miles_to_inspect
        
        transport.mileage = new_mileage
        
        transport.save()
        
        return transport
