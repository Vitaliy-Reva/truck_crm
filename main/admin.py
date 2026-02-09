from django.contrib import admin
from .models import Transport, Driver, Client, Trip, FuelLog, Maintenance, Order

admin.site.register(Transport)
admin.site.register(Driver)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Trip)
admin.site.register(FuelLog)
admin.site.register(Maintenance)
