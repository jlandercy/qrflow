from rest_framework import serializers

from flow import models


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Code
        fields = ['id', 'name', 'image']
