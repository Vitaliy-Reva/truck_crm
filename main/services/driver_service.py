from ..models import Driver

class DriverService:
    @staticmethod
    def create_driver(data: dict):
        return Driver.objects.create(**data)
    
    @staticmethod
    def updata_driver(driver: Driver):
        driver.save()
        return driver