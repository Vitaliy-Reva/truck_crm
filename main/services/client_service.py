from ..models import Client

class ClientService:
    @staticmethod
    def create_client(data: dict):
        return Client.objects.create(**data)
    
    @staticmethod
    def update_client(client: Client):
        client.save()
        return client
    
