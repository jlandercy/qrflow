from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class NoPermissionMixin(LoginRequiredMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.none()


class OrganizationPermissionMixin(LoginRequiredMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(
            organization__in=request.user.organization_set.all()
        )


class OrganizationMembershipPermissionMixin(LoginRequiredMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(
            organizationmembership__in=request.user.organizationmembership_set.all()
        )
