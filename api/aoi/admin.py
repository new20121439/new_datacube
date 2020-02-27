from django.contrib.gis import admin
from .models import AOI


admin.site.register(AOI, admin.GeoModelAdmin)
