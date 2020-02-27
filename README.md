
- Install gdal
    sudo aptitude install gdal-bin libgdal-dev
    sudo aptitude install python3-gdal
- Install enviroment: $ virtualenv <env_name> $ source <env_name>/bin/activate (<env_name>)$ pip install -r path/to/requirements.txt

- Change DIR in {project}/{project}/config.py:
    - DOWNLOAD_DIR, UPLOAD_DI, GRAPH_DIR, GPT_DIR, PRODUCT_DEFINITION_DIR

- Insall snap ESA (APP for processing sentinel-1)

- Notes:
    Error: from django.utils import six. ImportError: cannot import name 'six'. Solution: using import six instead of from django.utils import six
