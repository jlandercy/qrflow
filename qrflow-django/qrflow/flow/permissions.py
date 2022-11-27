from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from rest_framework import permissions

from core.permissions import BasePermissionMixin


class ApplicationPermissionMixin(BasePermissionMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(
            application__organization__in=request.user.organization_set.all()
        )


class CodePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        print(request)
        print(view)
        return True

    def has_object_permission(self, request, view, instance):
        print(request)
        print(view)
        print(instance)
        return False
