from django.contrib.gis.db import models
from django.core.validators import FileExtensionValidator
import uuid

upload_dir = 'upload/'

class UploadModel(models.Model):

    PRODUCT_CHOICES = (
        ('uav', 'UAV'),
    )
    title = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True)
    product_name = models.CharField(max_length=100, choices=PRODUCT_CHOICES)
    file = models.FileField(upload_to=upload_dir,
                            validators=[FileExtensionValidator(allowed_extensions=['tif'])])
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_time']

    def __str__(self):
        return self.title
