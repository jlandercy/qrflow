from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import SuspiciousOperation


class NoPermissionMixin(LoginRequiredMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.none()


class OrganizationPermissionMixin(LoginRequiredMixin, UserPassesTestMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(
            organization__in=request.user.organization_set.all()
        )

    def test_func(self):
        print(self)
        print(type(self))
        # MRO Will be the reason why!!!!
        return False

    def handle_no_permission(self):
        raise SuspiciousOperation("Go away Ana!")


class OrganizationMembershipPermissionMixin(LoginRequiredMixin):

    def get_queryset(self, *args, **kwargs):
        request = args[0] if args else kwargs.get('request') or self.request
        query = super().get_queryset(*args, **kwargs)
        if request.user.is_superuser:
            return query
        return query.filter(
            organizationmembership__in=request.user.organizationmembership_set.all()
        )
