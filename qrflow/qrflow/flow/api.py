from django.urls import path, include
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import permissions

from flow import models
from flow import serializers


app_name = 'flow'
router = routers.SimpleRouter()


class ApplicationViewSet(viewsets.ModelViewSet):

    permissions = (permissions.IsAuthenticated,)
    serializer_class = serializers.ApplicationSerializer
    queryset = models.Application.objects.all()


class CodeViewSet(viewsets.ModelViewSet):

    permissions = (permissions.IsAuthenticated,)
    serializer_class = serializers.CodeSerializer
    queryset = models.Code.objects.all()


class SinkAPIView(generics.GenericAPIView):

    def get(self, request, format=None):
        return Response({})


class QRCodeAPIView(generics.GenericAPIView):

    def get(self, request, format=None):
        return Response({})


router.register('application', viewset=ApplicationViewSet)
router.register('code', viewset=CodeViewSet)

urlpatterns = [
    path(r"code/sink/", SinkAPIView.as_view(), name="code-sink"),
]
