from django.contrib import admin
from .models import Transport, Driver, Trip, FuelLog, Maintenance

admin.site.register(Transport)
admin.site.register(Driver)
admin.site.register(Trip)
admin.site.register(FuelLog)
admin.site.register(Maintenance)
