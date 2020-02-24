import os
from .utils import get_name, make_dest_path
import gdal, gdalconst
from cogeotiff.cog import create_cog
from glob import glob
from celery import task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)


def merge_separate_bands(band_paths, name_file):
    """
    Merge seperate band (tif, jp2,...) into name_file.tif
    """
    print('Merge seperate bands')
    dest_path = os.path.dirname(band_paths[0]) + '/' + name_file + '.tif'
    if not os.path.exists(dest_path):
        cmd = 'gdal_merge.py -separate -a_nodata 0 -o {} {}'.format(dest_path, ' '.join(band_paths))
        os.system(cmd)
        for band_path in band_paths:
            if os.path.exists(band_path):
                os.remove(band_path)
    return dest_path

def get_subdataset(path):
    dataset = gdal.Open(path, gdal.GA_ReadOnly)
    sub_dataset = dataset.GetSubDatasets()[0]
    sub_dataset = sub_dataset[0]
    return sub_dataset

def zip_to_EPSG4326(dest_folder, path, keep_result_only=False):
    """
    Change GEOTIFF image path='folder/abc.zip' to 4326 GEOTIFF 'folder/abc_4326.tif'
    """
    name = get_name(path)
    dest_path = os.path.join(dest_folder, name + '_4326.tif')
    subset_path = get_subdataset(path)
    if not os.path.exists(dest_path):
        cmd = 'gdalwarp -t_srs EPSG:4326 -dstnodata 0 {0} {1}'.format(subset_path, dest_path)
        os.system(cmd)
    if keep_result_only:
        os.remove(path)
    return dest_path


@task(name="Process Image by Snap")
def process_by_snap(path, gpt='~/app/snap/bin/gpt', graph='/graph/graph_mlc_50m.xml'):
    logger.info(path, gpt, graph)
    dest_path = make_dest_path(path, '.tif')
    if not os.path.exists(gpt):
        raise FileNotFoundError('Must be set GPT path')
    if not os.path.exists(graph):
        raise FileNotFoundError('Must be set GRAPH path')
    if os.path.exists(dest_path):
        if os.path.getsize(dest_path) == 0:
            os.remove(dest_path)
            cmd = gpt + '  {} -Pinputfile={} -Poutputfile={}'.format(graph, path, dest_path)
            os.system(cmd)
    else:
        cmd = gpt + '  {} -Pinputfile={} -Poutputfile={}'.format(graph, path, dest_path)
        os.system(cmd)
    return dest_path

@task(name="Set metadata to dest image")
def set_metadata(dest_path, source_path):
    # Open the file:
    file_name = get_name(source_path)
    source_path = '/vsizip/{0}/{1}.SAFE'.format(source_path, file_name)
    source_ds = gdal.Open(source_path, gdalconst.GA_ReadOnly)
    metadata = source_ds.GetMetadata()
    gcp = source_ds.GetGCPs()
    gcpproj = source_ds.GetGCPProjection()

    ds = gdal.Open(dest_path, gdalconst.GA_Update)

    # resolution from 10m to 50m
    newgcp = [gdal.GCP(tmp.GCPX, tmp.GCPY, tmp.GCPZ, tmp.GCPPixel // 5, tmp.GCPLine // 5) for tmp in gcp]

    # set metadata
    ds.SetGCPs(newgcp, gcpproj)
    ds.SetMetadata(metadata)
    return dest_path

@task(name="Convert to EPSG: 4326")
def toEPSG4326(path, keep_result_only=False):
    """
    Change GEOTIFF image path='folder/abc.tif' to 4326 GEOTIFF 'folder/abc_4326.tif'
    """
    dest_path = make_dest_path(path, '_4326.tif')
    if not os.path.exists(dest_path):
        cmd = 'gdalwarp -t_srs EPSG:4326 -dstnodata 0 {0} {1}'.format(path, dest_path)
        os.system(cmd)
    if keep_result_only:
        os.remove(path)
    return dest_path

@task(name="Convert to Cloud Optimized Geotiff")
def toCOG(path, keep_result_only=False):
    """
    GEOTIFF path='folder/abc.tif' to CLOUD OPTIMIZED GEOTIFF 'folder/abc_cog.tif'
    """
    dest_path = make_dest_path(path, '_cog.tif')
    if not os.path.exists(dest_path):
        create_cog(path, dest_path, compress='LZW')
    if keep_result_only:
        for path__ in glob(path + '*'):
            if os.path.exists(path__):
                os.remove(path__)
    return dest_path


