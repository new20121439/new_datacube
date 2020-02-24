from rest_framework import serializers
from .models import UploadModel


class UploadSerializers(serializers.ModelSerializer):
    class Meta:
        model = UploadModel
        fields = '__all__'