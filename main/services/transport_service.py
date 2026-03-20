from ..models import Transport

class TransportService:
    @staticmethod
    def create_transport(data: dict):
        transport = Transport.objects.create(**data)
        transport.next_inspect = transport.mileage + transport.miles_to_inspect
        transport.save()
        return transport
    
    @staticmethod
    def update_transport(data: dict, transport: Transport):

        new_mileage = data["mileage"]
        
        if data is None:
            if new_mileage >= transport.next_inspect:
                transport.next_inspect += transport.miles_to_inspect
                transport.to = 'NS'
        
        transport.mileage = new_mileage

        for key, value in data.items():
            if hasattr(transport, key):
                setattr(transport, key, value)
        
        transport.save()
        
        return transport
