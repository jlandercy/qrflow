from django.contrib import admin
from django.utils.html import mark_safe, format_html

from core.admin import OrganizationAdminMixin
from flow import models


class ApplicationAdminMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(
            application__organization__in=request.user.organization_set.all()
        )


@admin.register(models.Application)
class ApplicationAdmin(OrganizationAdminMixin, admin.ModelAdmin):

    def _target_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.target)

    def _code_count(self, obj):
        return obj.code_set.count()

    list_display = ('id', 'organization', 'owner', 'name', '_target_url', '_code_count')
    search_fields = ('id', 'organization__id', 'organization__name', 'name')


@admin.register(models.Code)
class CodeAdmin(ApplicationAdminMixin, admin.ModelAdmin):

    def _base64(self, obj):
        return obj.base64[:128]

    def _image_tag(self, obj):
        return format_html('<a href="/media/{url}"><img src="/media/{url}" width="64px;" /></a>', url=obj.image)

    list_display = ('id', 'application', 'name', 'payload', '_image_tag')
    search_fields = ('id', 'application__id', 'application__name', 'name')
