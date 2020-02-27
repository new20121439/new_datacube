from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Model


def validate_aoi(value):
    if not isinstance(value, GEOSGeometry):
        raise ValidationError(
            '%(value)s is not an even number',
            params={'value': value},
        )


class AOI(models.Model):
    aoi = models.GeometryField(srid=4326, validators=[validate_aoi])

    def clean(self):
        if isinstance(self.aoi, GEOSGeometry):
            return self.aoi
        raise ValidationError(('Draft entries may not have a publication date.'))
        # return GEOSGeometry(self.aoi)
    def save(self, *args, **kwargs):
        self.clean()
        return super(AOI, self).save(*args, **kwargs)