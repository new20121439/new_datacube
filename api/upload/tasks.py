from api.ingest.tasks import ingest_data
from api.download.image_processing import toEPSG4326, toCOG
from celery import chain, task
from os.path import exists


@task(name='convert_to_EPSG4326_COG')
def toEPSG4326_COG(path):
    dest_path = path[:-4] + '_4326_cog.tif'
    if not exists(dest_path):
        task = chain(
            toEPSG4326.s(path, keep_result_only=False),
            toCOG.s(keep_result_only=True)
        ).apply_async()
        dest_path = task.get()
        print('dest_paht:_____',dest_path)
    return dest_path

def upload_process(product_name, dataset_path, uuid):
    print(dataset_path)
    dest_path = toEPSG4326_COG(dataset_path)
    print(dest_path)
    status = ingest_data(product_name, dest_path, uuid)
    return {
        'Status': status,
        'Message': 'Ingest to Datacube successfully'
    }