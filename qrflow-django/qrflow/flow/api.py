from django.shortcuts import get_object_or_404

#from myapps.serializers import UserSerializer

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import permissions

from flow import models
from flow import serializers
from flow.permissions import ApplicationPermissionMixin


router = routers.SimpleRouter()


class CodeViewSet(ApplicationPermissionMixin, viewsets.ModelViewSet):

    permissions = (permissions.IsAuthenticated,)
    serializer_class = serializers.CodeSerializer
    queryset = models.Code.objects.all()


router.register('code', viewset=CodeViewSet)
