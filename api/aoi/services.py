from .serializers import AOISerializers
from .models import AOI
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.gis.geos import GEOSGeometry


def list_aoi():
    aoi_objs = get_list_or_404(AOI)
    response = AOISerializers(instance=aoi_objs, many=True).data
    return response


def create_aoi(aoi):
    obj, created = AOI.objects.create(aoi=GEOSGeometry(aoi))

    return {
        "Status": "Success" if created else "Failed",
        "Message": "Create AOI {} ".format(aoi)
    }


def get_aoi(id):
    aoi_obj = get_object_or_404(AOI, pk=id)
    response = AOISerializers(instance=aoi_obj).data
    return response

