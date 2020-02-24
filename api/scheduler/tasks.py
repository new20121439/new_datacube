import datetime
from datetime import timedelta
from celery import task
from api.query.tasks import sentinel_query_task
from api.download.tasks import download_process
from api.ingest.tasks import ingest_data
"""
Wrap all process in one task, in order to register in celery beat
    - Query by (product_name, aoi) start_time and end_time: yesterday util now ---> list of dict or [] (in case that, result is empty)
    - If result is empty : break
    - ELse:
        - Select 1 of results ---> uuid
        - Download by product_name, uuid. Then, Ingest data
"""

@task(name='scheduler_task')
def scheduler_task(aoi, product_name):
    end_time = datetime.datetime.now().date()
    interval_1_day = timedelta(days=1)
    start_time = end_time - interval_1_day
    kwarg = {
        'product_name': product_name,
        'aoi': aoi,
        'start_time': start_time,
        'end_time': end_time
    }
    result = sentinel_query_task().query_aoi(**kwarg)
    if len(result) == 0:
        return False
    uuid = select_image(result)
    result_path = download_process(product_name, uuid)
    # ingest_data(product_name, result_path, uuid)
    return True

def select_image(list_images):
    """ Get the first image """
    return list_images[0]['uuid']