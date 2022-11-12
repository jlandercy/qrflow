from django.contrib import admin

from flow import models


@admin.register(models.Application)
class ApplicationAdmin(admin.ModelAdmin):

    def _code_count(self, obj):
        return obj.code_set.count()

    list_display = ('id', 'organization', 'owner', 'name', '_code_count')


@admin.register(models.Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'payload', 'image')
