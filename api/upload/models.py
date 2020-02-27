from django.contrib.gis.db import models
from django.core.validators import FileExtensionValidator
import uuid

upload_dir = 'upload/'

class UploadModel(models.Model):

    PRODUCT_CHOICES = (
        ('uav_30cm', 'UAV 30'),
    )
    title = models.CharField(max_length=100, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4(), unique=True)
    product_name = models.CharField(max_length=100, choices=PRODUCT_CHOICES)
    # file = models.FileField(upload_to=upload_dir,
    #                         validators=[FileExtensionValidator(allowed_extensions=['tif'])],
    #                         unique=True)
    file = models.ImageField(upload_to=upload_dir,
                            validators=[FileExtensionValidator(allowed_extensions=['tif'])],
                            unique=True,)
    upload_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-upload_time']

    def __str__(self):
        return self.title
