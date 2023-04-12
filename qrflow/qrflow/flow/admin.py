from django.contrib import admin
from django.utils.html import mark_safe, format_html

from flow import models


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):

    def _code_count(self, obj):
        return obj.code_count
    _code_count.admin_order_field = 'code_count'

    def _endpoint_count(self, obj):
        return obj.endpoint_count
    _code_count.admin_order_field = 'endpoint_count'

    list_display = ('id', 'organization', 'name', 'domain', '_code_count', '_endpoint_count')
    search_fields = ('id', 'organization__id', 'organization__name', 'domain')


@admin.register(models.Endpoint)
class EndpointAdmin(admin.ModelAdmin):

    list_display = ('id', 'application', 'name', 'method', 'target', 'parameters')
    search_fields = ('id', 'application__id', 'application__name', 'name', 'method', 'target')
    list_filter = ('application',)


@admin.register(models.Code)
class CodeAdmin(admin.ModelAdmin):

    def _base64(self, obj):
        return obj.base64[:128]

    def _image_tag(self, obj):
        return format_html('<a href="/media/{url}"><img src="/media/{url}" width="64px;" /></a>', url=obj.image)

    list_display = ('id', 'application', 'name', 'payload', '_image_tag', 'zorder')
    search_fields = ('id', 'application__id', 'application__name', 'name')
    list_editable = ('zorder',)
    list_filter = ('application',)
