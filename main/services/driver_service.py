from ..models import Driver

class DriverService:
    @staticmethod
    def driver_create(data: dict):
        data["first_name"] = data["first_name"].capitalize()
        data["last_name"] = data["last_name"].capitalize()

        return Driver.objects.create(**data)
    
    @staticmethod
    def driver_update(data: dict, driver: Driver):
        data["first_name"] = data["first_name"].capitalize()
        data["last_name"] = data["last_name"].capitalize()

        driver.save()
        
        return driver