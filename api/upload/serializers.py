from rest_framework import serializers
from .models import UploadModel


class UploadSerializers(serializers.ModelSerializer):
    path = serializers.SerializerMethodField('get_absolute_path')
    class Meta:
        model = UploadModel
        fields = '__all__'
        extra_fields = ['path']

    def get_absolute_path(self, obj):
        return obj.file.path