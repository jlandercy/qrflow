from rest_framework import serializers

from flow import models


class CodeSerializer(serializers.ModelSerializer):

    def get_base64(self, obj):
        return obj.base64

    base64 = serializers.SerializerMethodField()

    class Meta:
        model = models.Code
        fields = ['id', 'name', 'image', 'base64']
