from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):

    def _users(self, obj):
        print(dir(obj))
        return ", ".join([item.username for item in obj.users.all()])

    list_display = ('id', 'name', '_users')


@admin.register(models.OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organization')
