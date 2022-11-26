from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core import models


class OrganizationAdminMixin:

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            organization__in=request.user.organization_set.all()
        )


class OrganizationMembershipAdminMixin:

    def get_queryset(self, request):
        return super().get_queryset(request).filter(
            organizationmembership__in=request.user.organizationmembership_set.all()
        )


@admin.register(models.CustomUser)
class CustomUserAdmin(OrganizationMembershipAdminMixin, UserAdmin):
    pass


@admin.register(models.Organization)
class OrganizationAdmin(OrganizationMembershipAdminMixin, admin.ModelAdmin):

    def _users(self, obj):
        return ", ".join([item.username for item in obj.users.all()])

    list_display = ('id', 'name', '_users')


@admin.register(models.OrganizationMembership)
class OrganizationMembershipAdmin(OrganizationAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'organization')
