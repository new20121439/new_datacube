from datacube import Datacube



def list_product():
    response = Datacube().list_products().to_dict('record')
    return response

