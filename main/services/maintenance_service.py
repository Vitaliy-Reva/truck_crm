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
        
        transport.save()

        return maintenance
    
    @staticmethod
    def maintenance_update(data: dict, maintenance: Maintenance, transport: Transport):
        data["transport_id"] = transport
        if maintenance.type == 'S':
            transport.to = 'OS'
        if maintenance.type == 'R':
            transport.to = 'R'
        
        transport.save()
        maintenance.save()
        return maintenance