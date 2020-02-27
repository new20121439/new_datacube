from .models import AOI
from rest_framework import serializers


class AOISerializers(serializers.ModelSerializer):
    class Meta:
        model = AOI
        fields = '__all__'

