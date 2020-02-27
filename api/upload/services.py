from .models import UploadModel
from .serializers import UploadSerializers
from .tasks import upload_process
from os.path import exists
import os


def list_uploads():
    upload_objs = UploadModel.objects
    response = UploadSerializers(instance=upload_objs, many=True).data
    return response


def create_upload(title, product_name, file):
    try:
        if UploadModel.objects.filter(title=title).exists():
            return {
                'Status': 'Success',
                'Message': 'File is already exist'
            }
        obj = UploadModel.objects.create(title=title, product_name=product_name, file=file)
        obj_serializers = UploadSerializers(instance=obj).data
        upload_process(obj_serializers['product_name'], obj_serializers['path'], obj_serializers['uuid'])
        return {
            'Status': 'Success',
            'Message': 'Upload file successfully'
        }
    except Exception as e:
        try:
            file_path = obj.file.path
            if exists(file_path):
                print('Deleting upload file')
                os.remove(file_path)
            obj.delete()
        except NameError:
            pass
        return {
            'Status': 'Failed',
            'Message': str(e)
        }


def get_upload(id):
    try:
        upload_obj = UploadModel.objects.get(pk=id)
        response = UploadSerializers(instance=upload_obj, many=False).data
        return response
    except Exception as e:
        return {
            'Status': 'Failed',
            'Message': 'Not found upload file ' + str(id)
        }
