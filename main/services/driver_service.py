from ..models import Driver

class DriverService:
    @staticmethod
    def driver_create(data: dict):
        return Driver.objects.create(**data)
    
    @staticmethod
    def driver_update(driver: Driver):
        driver.save()
        return driver