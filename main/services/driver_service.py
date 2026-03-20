from ..models import Driver

class DriverService:
    @staticmethod
    def driver_create(data: dict):
        data["first_name"] = data["first_name"].capitalize()
        data["last_name"] = data["last_name"].capitalize()

        return Driver.objects.create(**data)
    
    @staticmethod
    def driver_update(data: dict, driver: Driver):
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        if first_name or last_name:
            data["first_name"] = first_name.capitalize()
            data["last_name"] = last_name.capitalize()

        for key, value in data.items():
            if hasattr(driver, key):
                setattr(driver, key, value)

        driver.save()
        
        return driver