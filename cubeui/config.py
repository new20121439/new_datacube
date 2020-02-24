import os
from os.path import join, dirname, abspath

BASE_DIR = dirname(dirname(abspath(__file__)))
OUTER_BASE_DIR = dirname(BASE_DIR)

MEDIA_DIR = join(OUTER_BASE_DIR, "datacube/media/")
DOWNLOAD_DIR = join(OUTER_BASE_DIR, "datacube/original_data/")
UPLOAD_DIR = join(OUTER_BASE_DIR, "datacube/upload/")
GRAPH_DIR = join(BASE_DIR, "api/download/graph/")
GPT_DIR = '/home/dung/Datacube/snap/bin/gpt'
PRODUCT_DEFINITION_DIR = join(BASE_DIR, "api/ingest/product/")
GOOGLE_CLOUD_CRIDENTIAL = join(BASE_DIR, "api/download/cridential/sentinel2-gcs.json")