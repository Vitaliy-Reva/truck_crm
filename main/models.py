from django.db import models

class Transport(models.Model):
    id = models.IntegerField(max_length=100, primary_key=True)
    transport_model = models.CharField(max_length=40, null=False)
    license_plate = models.CharField(max_length=8, null=False)
    fuel_rate = models.SmallIntegerField(max_length=8, null=False)
    vin = models.CharField(max_length=17, null=False)
    mileage = models.SmallIntegerField(max_length=10, null=False)
    status = models.CharField(max_length=15, null=False)

    class Meta:
        ordering = ('name',)
        verbose_name = "Транспорт"
        verbose_name_plural = "Транспорти"
    
    def __str__(self):
        return self.name


class Driver(models.Model):
    id = models.IntegerField(max_length=100, primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    license = models.CharField(max_length=100, null=False)
    experience = models.TextField(max_length=500)
    phone = models.CharField(max_length=13, null=False)

    class Meta:
        ordering = ('name',)
        verbose_name = "Водій"
        verbose_name_plural = "Водії"
    
    def __str__(self):
        return self.name


class Trip(models.Model):
    id = models.IntegerField(max_length=100, primary_key=True)
    driver_id = models.ForeignKey(Driver, on_delete=models.CASCADE)
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    start_point = models.CharField(max_length=20, null=False)
    end_point = models.CharField(max_length=20, null=False)
    status = models.CharField(max_length=15, null=False)
    distance = models.IntegerField(max_length=5, null=False)
    fuel_planned = models.IntegerField(max_length=5, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Поїздка"
        verbose_name_plural = "Поїздки"
    
    def __str__(self):
        return self.name


class FuelLog(models.Model):
    id = models.IntegerField(max_length=100, primary_key=True)
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE)
    liters = models.IntegerField(max_length=10, null=False)
    price = models.DecimalField(max_length=15, null=False)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ('name',)
        verbose_name = "Паливо"
        verbose_name_plural = "Палива"
    
    def __str__(self):
        return self.name


class Maintenance(models.Model):
    id = models.IntegerField(max_length=100, primary_key=True)
    transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    type = models.CharField(max_length=15, null=False)
    cost = models.DecimalField(max_length=10, null=False)
    date = models.DateField()

    class Meta:
        ordering = ('name',)
        verbose_name = "Технічне обслуговування"
        verbose_name_plural = "Технічні обслуговування"
    
    def __str__(self):
        return self.name