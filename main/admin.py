from django.contrib import admin
from .models import *

admin.site.register(Transport)
admin.site.register(Driver)
admin.site.register(Client)
admin.site.register(Order)
admin.site.register(Trip)
admin.site.register(FuelLog)
admin.site.register(Maintenance)
admin.site.register(NoPayedOrder)
