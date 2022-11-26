from django.contrib.auth.mixins import PermissionRequiredMixin


class NoPermissionMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.none()


class OrganizationPermissionMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(
            organization__in=request.user.organization_set.all()
        )


class OrganizationMembershipPermissionMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(
            organizationmembership__in=request.user.organizationmembership_set.all()
        )
