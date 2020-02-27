from .models import DownloadModel
from django.core.serializers import serialize
from .tasks import sentinel_query_task
import datetime
import json


def create_download(uuid, path_in, path_COG):
    product_odata = sentinel_query_task().get_product_odata(uuid)
    paras = {
        'uuid': product_odata['id'],
        'title': product_odata['title'],
        'creation_date': product_odata['Creation Date'],
        'ingestion_date': product_odata['Ingestion Date'],
        'footprint': product_odata['footprint'],
        'link': product_odata['url'],
        'size': product_odata['size'],
        'original_image_src': path_in,
        'processed_image_src': path_COG,
        'end_execution_time': datetime.datetime.now()
    }
    print(paras)
    query_set = DownloadModel.objects.get_or_create(**paras)

def list_download():
    query_set = DownloadModel.objects.all()
    response = serialize('json', query_set)
    return json.loads(response)