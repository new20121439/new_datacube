import rasterio.warp
from osgeo import osr
from pathlib import Path
from datacube.index.hl import Doc2Dataset
import datacube

# Construct metadata dict
from uuid import uuid4
from dateutil import parser
from api.mylib.utils import get_name


class Data_index:
    dc = datacube.Datacube()

    def __init__(self, name_product, ):
        self.name_product = name_product

    def product_definition(self):
        dataset_type = self.dc.index.products.get_by_name(self.name_product)
        if not dataset_type:
            raise NotImplementedError(
                "Product definition {} is not available. You must add the product ".format(self.name_product)
            )
        return dataset_type.definition

    def get_date(self, dataset_path, start_time_idx=2, end_time_idx=6):
        name = get_name(dataset_path)
        arr = name.split('_')
        return (parser.parse(arr[start_time_idx]), parser.parse(arr[end_time_idx]))

    def get_geometry(self, dataset_path):
        with rasterio.open(dataset_path) as img:
            left, bottom, right, top = img.bounds
            crs = str(str(getattr(img, 'crs_wkt', None) or img.crs.wkt))
            corners = {
                'ul': {
                    'x': left,
                    'y': top
                },
                'ur': {
                    'x': right,
                    'y': top
                },
                'll': {
                    'x': left,
                    'y': bottom
                },
                'lr': {
                    'x': right,
                    'y': bottom
                }
            }
            projection = {'spatial_reference': crs, 'geo_ref_points': corners}

            spatial_ref = osr.SpatialReference(crs)
            t = osr.CoordinateTransformation(spatial_ref, spatial_ref.CloneGeogCS())

            def transform(p):
                lon, lat, z = t.TransformPoint(p['x'], p['y'])
                return {'lon': lon, 'lat': lat}

            extent = {key: transform(p) for key, p in corners.items()}

            return projection, extent


    def index(self, dataset_path, uuid=None):
        product_def = self.product_definition()
        if self.dc.index.datasets.has(uuid):
            print('uuid is already exist')
            return True

        resolver = Doc2Dataset(self.dc.index)
        projection, extent = self.get_geometry(dataset_path)
        (t0, t1) = self.get_date(dataset_path)

        images = {measurements['name']: {'path': dataset_path, 'layer': i + 1} for i, measurements in
                  enumerate(product_def['measurements'])}
        p = Path(dataset_path)
        scene_name = p.stem[:-11]
        result = {
            # Generate random uuid()
            'id': str(uuid) if uuid else str(uuid4()),
            'processing_level': product_def['metadata']['processing_level'],
            'product_type': product_def['metadata']['product_type'],
            'creation_dt': t0,
            'platform': product_def['metadata']['platform'],
            'instrument': product_def['metadata']['instrument'],
            'extent': {
                'coord': extent,
                'from_dt': str(t0),
                'to_dt': str(t1),
                'center_dt': str(t0 + (t1 - t0) / 2)
            },
            'format': product_def['metadata']['format'],
            'grid_spatial': {
                'projection': projection
            },
            'image': {
                'bands': images
            },
            'lineage': {
                'source_datasets': {},
                'ga_label': scene_name
            }
        }
        print(result)
        dataset, _ = resolver(result, '')
        print(dataset)
        self.dc.index.datasets.add(dataset)
        return True


class sentinel2_index(Data_index):
    def get_date(self, dataset_path, start_time_idx=2, end_time_idx=6):
        name = get_name(dataset_path)
        arr = name.split('_')
        return (parser.parse(arr[start_time_idx]), parser.parse(arr[end_time_idx]))


class sentinel1_index(Data_index):
    def get_date(self, dataset_path, start_time_idx=4, end_time_idx=5):
        name = get_name(dataset_path)
        arr = name.split('_')
        return (parser.parse(arr[start_time_idx]), parser.parse(arr[end_time_idx]))

class uav_index(Data_index):
    def get_date(self, dataset_path, start_time_idx=2, end_time_idx=3):
        name = get_name(dataset_path)
        arr = name.split('_')
        return (parser.parse(arr[start_time_idx]), parser.parse(arr[end_time_idx]))


sentinel_2_l2a = "sentinel_2_l2a"
sentinel_1_grd_50m_beta0 = "sentinel_1_grd_50m_beta0"
uav_30cm = "uav_30cm"
def ingest_data(product_name, dataset_path, uuid):
    status = 'Failed'
    try:
        if product_name == sentinel_1_grd_50m_beta0:
            sentinel1_index(product_name).index(dataset_path, uuid)
            status = 'Success'
        if product_name == sentinel_2_l2a:
            sentinel2_index(sentinel_2_l2a).index(dataset_path, uuid)
            status = 'Success'
        if product_name == uav_30cm:
            uav_index(uav_30cm).index(dataset_path, uuid)
            status = 'Success'
    except Exception:
        pass

    return status