from django.contrib import admin
from .models import *
from django.contrib.gis import admin

# Register your models here.
class MyModelAdmin(admin.OSMGeoAdmin):
    pass
admin.site.register(WorkshopAccount,MyModelAdmin)
admin.site.register(BookingDetails)