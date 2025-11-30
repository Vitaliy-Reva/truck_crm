from django.contrib import admin
from .models import Transport, Driver, Trip, FuelLog, Maintenance

admin.site.register(Transport, Driver, Trip, FuelLog, Maintenance)