from django.shortcuts import get_object_or_404

#from myapps.serializers import UserSerializer

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import permissions

from flow import models
from flow import serializers
from core.permissions import OrganizationPermissionMixin
from flow.permissions import ApplicationPermissionMixin, CodePermission


router = routers.SimpleRouter()


class ApplicationViewSet(OrganizationPermissionMixin, viewsets.ModelViewSet):

    permissions = (permissions.IsAuthenticated,)
    serializer_class = serializers.ApplicationSerializer
    queryset = models.Application.objects.all()


class CodeViewSet(ApplicationPermissionMixin, viewsets.ModelViewSet):

    permissions = (permissions.IsAuthenticated, CodePermission,)
    serializer_class = serializers.CodeSerializer
    queryset = models.Code.objects.all()


class QRCodeAPIView(generics.GenericAPIView):

    def get(self, request, format=None):
        return Response({})


router.register('application', viewset=ApplicationViewSet)
router.register('code', viewset=CodeViewSet)
#router.register('code/generate', QRCodeAPIView.as_view(), basename='code_generate')
