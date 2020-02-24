from .models import UploadModel
from .serializers import UploadSerializers


def list_uploads():
    upload_objs = UploadModel.objects
    response = UploadSerializers(instance=upload_objs, many=True).data
    return response


def create_upload(title, product_name, file):
    UploadModel.objects.get_or_create(title=title, product_name=product_name, file=file)
    return {
        'status': 'Success'
    }


def get_upload(id):
    try:
        upload_obj = UploadModel.objects.get(pk=id)
        response = UploadSerializers(instance=upload_obj, many=False).data
        return response
    except Exception as e:
        print(e)
        return {
            'status': 'false',
            'message': 'Not found upload file ' + str(id)
        }
