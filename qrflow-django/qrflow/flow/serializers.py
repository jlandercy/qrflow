from rest_framework import serializers

from flow import models


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Application
        fields = ('id', 'name', 'organization')


class CodeSerializer(serializers.ModelSerializer):

    def get_base64(self, obj):
        return obj.base64

    organization = serializers.UUIDField(source='application.organization.id', required=False)
    base64 = serializers.SerializerMethodField()

    class Meta:
        model = models.Code
        fields = ('id', 'name', 'application', 'organization', 'payload', 'image', 'base64')
