from ..models import Maintenance, Transport

class MaintenanceService:
    @staticmethod
    def maintenance_create(data: dict, transport: Transport):
        data["transport_id"] = transport
        maintenance = Maintenance.objects.create(**data)

        if maintenance.type == 'S':
            transport.to = 'OS'
        if maintenance.type == 'R':
            transport.to = 'R'
        if maintenance.type == 'E':
            transport.to = 'S'
        
        transport.save()

        return maintenance
    
    @staticmethod
    def maintenance_update(data: dict, maintenance: Maintenance, transport: Transport):
        data["transport_id"] = transport
        new_type = data.get("type", maintenance.type)

        if new_type == 'S':
            transport.to = 'OS'
        if new_type == 'R':
            transport.to = 'R'
        if new_type == 'E':
            transport.to = 'S'

        for key, value in data.items():
            if hasattr(maintenance, key):
                setattr(maintenance, key, value)

        transport.save()
        maintenance.save()
        
        return maintenance