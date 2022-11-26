from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from core import models


class OrganizationAdminMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(
            organization__in=request.user.organization_set.all()
        )


class OrganizationMembershipAdminMixin:

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.filter(
            organizationmembership__in=request.user.organizationmembership_set.all()
        )


@admin.register(models.CustomUser)
class CustomUserAdmin(OrganizationMembershipAdminMixin, UserAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if request.user.is_superuser:
            return query
        return query.none()

    def _user(self, obj):
        session_user = obj.get_decoded().get('_auth_user_id')
        user = models.CustomUser.objects.get(pk=session_user)
        return user

    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ('_user', 'session_key', '_session_data', 'expire_date')
    readonly_fields = ('_session_data',)
    exclude = ('session_data',)
    date_hierarchy = 'expire_date'


@admin.register(models.Organization)
class OrganizationAdmin(OrganizationMembershipAdminMixin, admin.ModelAdmin):

    def _users(self, obj):
        return ", ".join([item.username for item in obj.users.all()])

    list_display = ('id', 'name', '_users')


@admin.register(models.OrganizationMembership)
class OrganizationMembershipAdmin(OrganizationAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'user', 'organization')
