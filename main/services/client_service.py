from ..models import Client

class ClientService:
    @staticmethod
    def create_client(data: dict):
        data["first_name"] = data["first_name"].capitalize()
        data["last_name"] = data["last_name"].capitalize()

        return Client.objects.create(**data)
    
    @staticmethod
    def update_client(data: dict, client: Client):
        data["first_name"] = data["first_name"].capitalize()
        data["last_name"] = data["last_name"].capitalize()

        client.save()
        
        return client
    
