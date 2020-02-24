from sentinelsat import SentinelAPI, geojson_to_wkt
from geojson import Polygon
import datetime
import os


class sentinel_query_task:
    user = 'tranvandung20121439'
    password = 'dung20121439'
    api_url = 'https://scihub.copernicus.eu/dhus'
    api = SentinelAPI(user, password, api_url)

    def query(self, product_name,  min_lon, max_lon, min_lat, max_lat, start_time, end_time):
        plat_product = get_platform_producttype(product_name)
        platformname, product_type = plat_product['platformname'], plat_product['product_type']

        min_lon, max_lon, min_lat, max_lat = self.validate_coord(min_lon), self.validate_coord(max_lon), self.validate_coord(min_lat), self.validate_coord(max_lat)
        extent = Polygon([[(min_lon, max_lat),
                           (max_lon, max_lat),
                           (max_lon, min_lat),
                           (min_lon, min_lat),
                           (min_lon, max_lat)]])
        extent = geojson_to_wkt(extent)
        start_time, end_time = self.validate_date(start_time), self.validate_date(end_time)
        extra_dict = {}
        if platformname in ['Sentinel-2', 'SENTINEL-2']:
            extra_dict = {'cloudcoverpercentage': (0, 10)}
        products = self.api.query(extent,
                             date=(start_time, end_time),
                             area_relation='Intersects',
                             platformname=platformname,
                             producttype=product_type,
                            **extra_dict
                            )
        products_df = self.api.to_dataframe(products)
        print(products_df)
        if products_df.empty:
            return {}
        return products_df.to_dict('record')

    def query_aoi(self, product_name,  aoi, start_time, end_time):
        plat_product = get_platform_producttype(product_name)
        platformname, product_type = plat_product['platformname'], plat_product['product_type']
        start_time, end_time = self.validate_date(start_time), self.validate_date(end_time)
        extra_dict = {}
        if platformname in ['Sentinel-2', 'SENTINEL-2']:
            extra_dict = {'cloudcoverpercentage': (0, 10)}
        products = self.api.query(aoi,
                             date=(start_time, end_time),
                             area_relation='Intersects',
                             platformname=platformname,
                             producttype=product_type,
                            **extra_dict
                            )
        products_df = self.api.to_dataframe(products)
        print(products_df)
        if products_df.empty:
            return []
        return products_df.to_dict('record')


    def validate_date(self, date):
        if type(date) is str:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        return date

    def validate_coord(self, x):
        return float(x)

    def get_title_by_uuid(self, uuid):
        product_odata = self.api.get_product_odata(uuid)
        return product_odata['title']

    def get_product_odata(self, uuid):
        return self.api.get_product_odata(uuid)

    def download(self, uuid, directory_path, file_format='zip'):
        dest_download_path = directory_path + '/' + self.get_title_by_uuid(uuid) + '.' + file_format
        if not os.path.exists(dest_download_path):
            dest_download_path = self.api.download(uuid, directory_path)
        return dest_download_path


def get_platform_producttype(product_name):
    if product_name == "sentinel_2_l2a":
        return {
            'platformname': 'Sentinel-2',
            'product_type': 'S2MSI2A'
        }
    elif product_name == "sentinel_1_grd_50m_beta0":
        return {
            'platformname': 'Sentinel-1',
            'product_type': 'GRD'
        }
    else:
        raise Exception("Do not have this product. Please, choose another option")


# def query_task(product_name, min_lon, max_lon, min_lat, max_lat, start_time, end_time):
#     # response = sentinel_query_task().query(product_name,
#     #                                        min_lon, max_lon, min_lat, max_lat, start_time, end_time)
#     r = {'body': response}
#     return r

def query_task(product_name, aoi, start_time, end_time):
    response = sentinel_query_task().query_aoi(product_name, aoi, start_time, end_time)
    r = {'body': response}
    return r