import os
from .models import DownloadModel
from .download import sentinel2_google_cloud
from .image_processing import (toEPSG4326, toCOG, process_by_snap, set_metadata)
from celery import task, chain
from api.query.tasks import sentinel_query_task
from api.query.views import get_platform_producttype
from api.ingest.tasks import ingest_data
from .services import create_download

from cubeui.config import GRAPH_DIR, GPT_DIR, DOWNLOAD_DIR



gpt = GPT_DIR
graph = GRAPH_DIR + 'graph_mlc_50m.xml'
dest_download_dir = DOWNLOAD_DIR

@task(name='download_from_cloud')
def download_from_cloud(title, dest_download_dir):
    path_tif = sentinel2_google_cloud(title).download(dest_download_dir)
    return path_tif

@task(name='download_from_scihub')
def download_from_scihub(uuid, dest_download_dir):
    path_zip = sentinel_query_task().download(uuid, dest_download_dir, 'zip')
    return path_zip



@task(name='sentinel_2_download_process')
def sentinel_2_download_process(uuid, dest_download_dir):
    title = sentinel_query_task().get_title_by_uuid(uuid)
    path_tif = dest_download_dir + '/' + title + '.tif'
    path_COG = dest_download_dir + '/' + title + '_4326_cog.tif'
    if not os.path.exists(path_COG):
        task = chain(
            download_from_cloud.s(title, dest_download_dir),
            toEPSG4326.s(keep_result_only=False),
            toCOG.s(keep_result_only=True)
        ).apply_async()
        path_tif, path_COG = task.parent.parent.get(), task.get()
        create_download(uuid, path_tif, path_COG)
    return path_tif, path_COG


@task(name='sentinel_1_download_process')
def sentinel_1_download_process(uuid, dest_download_dir):
    title = sentinel_query_task().get_title_by_uuid(uuid)
    path_zip = dest_download_dir + '/' + title + '.zip'
    path_COG = dest_download_dir + '/' + title + '_4326_cog.tif'
    if not os.path.exists(path_COG):
        task = chain(
            download_from_scihub.s(uuid, dest_download_dir),
            process_by_snap.s(gpt, graph),
            set_metadata.s(path_zip),
            toEPSG4326.s(keep_result_only=True),
            toCOG.s(keep_result_only=True)
        ).apply_async()
        path_zip, path_COG = task.parent.parent.parent.parent.get(), task.get()
        create_download(uuid, path_zip, path_COG)
    return path_zip, path_COG

def check_image_db(uuid):
    if DownloadModel.objects.filter(uuid=uuid).count() > 0:
        return True
    return False

@task(name='Download')
def download_process(product_name, uuid):
    # if not check_image_db(uuid):
    plat_product = get_platform_producttype(product_name)
    platformname = plat_product['platformname']
    if platformname in ['SENTINEL-2', 'Sentinel-2']:
        path_in, path_COG = sentinel_2_download_process(uuid, dest_download_dir)  # path_in .tif
    if platformname in ['SENTINEL-1', 'Sentinel-1']:
        path_in, path_COG = sentinel_1_download_process(uuid, dest_download_dir)   #p path_in .zip

    """ Index dataset at the same time"""
    status = ingest_data(product_name, path_COG, uuid)
    return {
        'Status': status,
        'Message': 'Ingest to Datacube successfully'
    }
