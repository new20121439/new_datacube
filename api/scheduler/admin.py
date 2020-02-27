from django.contrib.gis import admin
from .models import Scheduler


admin.site.register(Scheduler, admin.GeoModelAdmin)