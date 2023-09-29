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

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['organization'].queryset = request.user.organization_set.all()
        return form


class RelatedOrganizationPermissionMixin(BasePermissionMixin):

    related_organization_field = None
    related_filtered_fields = []

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        return query.filter(**{
            (self.related_organization_field + "__organization__in"): request.user.organization_set.all()
        })

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for config in self.related_filtered_fields:
            form.base_fields[config["field"]].queryset = config["factory"].filter(organization__in=request.user.organization_set.all())
        return form
