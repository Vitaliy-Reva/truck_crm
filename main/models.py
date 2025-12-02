from django.db import models

class Transport(models.Model):
    transport_model = models.CharField(max_length=40, null=False)
    license_plate = models.CharField(max_length=10, null=False)
    fuel_rate = models.IntegerField(null=False)
    vin = models.CharField(max_length=17, null=False, unique=True)
    mileage = models.SmallIntegerField(null=False)
    status = models.CharField(max_length=15, null=False)

    class Meta:
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорти"
    
    def __str__(self):
        return f"{self.transport_model} ({self.license_plate})"


class Driver(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    license = models.CharField(max_length=100, null=False)
    itn = models.CharField(max_length=10, null=False, unique=True)
    experience = models.TextField(max_length=500)
    phone = models.CharField(max_length=13, null=False)

    class Meta:
        verbose_name = "Водій"
        verbose_name_plural = "Водії"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"


class Trip(models.Model):
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    start_point = models.CharField(max_length=20, null=False)
    end_point = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=15, null=False)
    distance = models.IntegerField(null=False)
    fuel_planned = models.IntegerField(null=True)

    class Meta:
        verbose_name = "Поїздка"
        verbose_name_plural = "Поїздки"
    
    def __str__(self):
        return f"{self.start_point} - {self.end_point} ({self.status})"


class FuelLog(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    liters = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name = "Паливо"
        verbose_name_plural = "Палива"
    
    def __str__(self):
        return f"{self.liters} ({self.price} грн)"


class Maintenance(models.Model):
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, null=False)
    cost = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    date = models.DateField()

    class Meta:
        verbose_name = "Технічне обслуговування"
        verbose_name_plural = "Технічні обслуговування"
    
    def __str__(self):
        return f"{self.type} ({self.cost})"