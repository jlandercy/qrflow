from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import SuspiciousOperation

from rest_framework import permissions


class BasePermissionMixin(LoginRequiredMixin, object):
    pass


class NoPermissionMixin(BasePermissionMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.none()


class OrganizationPermissionMixin(BasePermissionMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(
            organization__in=request.user.organization_set.all()
        )


class RelatedOrganizationPermissionMixin(BasePermissionMixin):

    related_organization_field = None

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(**{
            (self.related_organization_field + "__organization__in"): request.user.organization_set.all()
        })

#
# class OrganizationMembershipPermissionMixin(BasePermissionMixin):
#
#     def get_queryset(self, *args, **kwargs):
#         request = args[0] if args else kwargs.get('request') or self.request
#         query = super().get_queryset(*args, **kwargs)
#         if request.user.is_superuser:
#             return query
#         return query.filter(
#             organizationmembership__in=request.user.organizationmembership_set.all()
#         )
