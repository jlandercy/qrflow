from django.contrib.auth.mixins import PermissionRequiredMixin


class ApplicationPermissionMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(
            application__organization__in=request.user.organization_set.all()
        )
