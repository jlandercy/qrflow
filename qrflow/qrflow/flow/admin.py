from django.contrib import admin
from django.utils.html import mark_safe, format_html

from flow import models
from core.models import Organization
from core.permissions import OrganizationPermissionMixin, RelatedOrganizationPermissionMixin


@admin.register(models.Application)
class ApplicationAdmin(OrganizationPermissionMixin, admin.ModelAdmin):

    def _code_count(self, obj):
        return obj.code_count
    _code_count.admin_order_field = 'code_count'

    def _endpoint_count(self, obj):
        return obj.endpoint_count
    _code_count.admin_order_field = 'endpoint_count'

    def _domain(self, obj):
        return mark_safe('<a href="{url:}" target="_blank">{url:}</a>'.format(url=obj.domain))

    list_display = ('id', 'organization', 'name', '_domain', '_code_count', '_endpoint_count')
    search_fields = ('id', 'organization__id', 'organization__name', 'domain')


class ApplicationListFilter(admin.SimpleListFilter):

    title = "Applications"
    parameter_name = 'application'

    def lookups(self, request, model_admin):
        return [
            (item.id, item.name)
            for item in models.Application.objects.filter(
                organization__in=request.user.organization_set.all()
            )
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(application=self.value())
        return queryset


@admin.register(models.Endpoint)
class EndpointAdmin(RelatedOrganizationPermissionMixin, admin.ModelAdmin):

    related_organization_field = "application"
    related_filtered_fields = [
        {"field": related_organization_field, "factory": models.Application.objects.all()},
    ]

    related_organization_field = "application"
    list_display = ('id', 'application', 'name', 'method', 'target', 'parameters')
    search_fields = ('id', 'application__id', 'application__name', 'name', 'method', 'target')
    list_filter = (ApplicationListFilter,)


@admin.register(models.Code)
class CodeAdmin(RelatedOrganizationPermissionMixin, admin.ModelAdmin):

    def _base64(self, obj):
        return obj.base64[:128]

    def _image_tag(self, obj):
        return format_html('<a href="/media/{url}"><img src="/media/{url}" width="64px;" /></a>', url=obj.image)

    related_organization_field = "application"
    related_filtered_fields = [
        {"field": related_organization_field, "factory": models.Application.objects.all()},
    ]

    list_display = ('id', 'application', 'name', 'endpoint', 'payload', '_image_tag', 'zorder')
    search_fields = ('id', 'application__id', 'application__name', 'name')
    list_editable = ('zorder',)
    list_filter = (ApplicationListFilter,)
