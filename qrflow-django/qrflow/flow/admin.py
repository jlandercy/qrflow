from django.contrib import admin
from django.utils.html import mark_safe, format_html


from flow import models


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):

    def _target_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.target)

    def _code_count(self, obj):
        return obj.code_set.count()

    list_display = ('id', 'organization', 'owner', 'name', '_target_url', '_code_count')


@admin.register(models.Code)
class CodeAdmin(admin.ModelAdmin):

    def _image_tag(self, obj):
        return mark_safe('<img src="/media/%s" width="64px;" />' % obj.image)

    list_display = ('id', 'application', 'name', 'payload', 'image', '_image_tag')
