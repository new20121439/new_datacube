import datacube

dc = datacube.Datacube()

def get_all_products():
    list_products = dc.list_products()
    return list_products