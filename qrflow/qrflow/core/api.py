
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import permissions

from core import models
from core import serializers


router = routers.SimpleRouter()

#
# class OrganizationViewSet(viewsets.ModelViewSet):
#
#     permissions = (permissions.IsAuthenticated,)
#     serializer_class = serializers.OrganizationSerializer
#     queryset = models.Organization.objects.all()
#
#
# router.register('organization', viewset=OrganizationViewSet)
