from django.contrib.gis.db import models
import datetime
# Create your models here.

class DownloadModel(models.Model):
    uuid = models.UUIDField(unique=True)
    title = models.CharField(name='title', max_length=80, default="")
    creation_date = models.DateField('Creation Date')
    ingestion_date = models.DateField('Ingestion Date')
    footprint = models.GeometryField(srid=4326)
    link = models.CharField(max_length=200, default="")
    size = models.CharField(max_length=30, default="0 GB")
    original_image_src = models.CharField(max_length=200, default='')
    processed_image_src = models.CharField(max_length=200, default='')
    end_execution_time = models.DateTimeField('end_execution_time', default=datetime.datetime.now)

"""
product_odata of SENTINEL

{'id': '619e1bd7-0987-4c4f-a6f5-cf69d75957dc',
 'title': 'S2A_MSIL2A_20190306T094031_N0211_R036_T32PPS_20190306T141347',
 'size': 1031220910,
 'md5': 'A71C2B337C07531CEC99761661EF4920',
 'date': datetime.datetime(2019, 3, 6, 9, 40, 31, 24000),
 'footprint': 'POLYGON((10.91420138206751 10.03106739221819,10.89348533946126 9.940768920752854,10.874537808228643 9.857145704844665,9.912025184585323 9.861176010788647,9.914900098204498 10.854121391354942,10.919171426317744 10.84949792011836,10.91420138206751 10.03106739221819))',
 'url': "https://scihub.copernicus.eu/dhus/odata/v1/Products('619e1bd7-0987-4c4f-a6f5-cf69d75957dc')/$value",
 'Online': True,
 'Creation Date': datetime.datetime(2019, 3, 7, 2, 16, 59, 771000),
 'Ingestion Date': datetime.datetime(2019, 3, 7, 2, 5, 50, 584000)}
"""