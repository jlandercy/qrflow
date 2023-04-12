from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from core import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    class Meta:
        model = UserAdmin


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):

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

#
# @admin.register(models.Organization)
# class OrganizationAdmin(admin.ModelAdmin):
#
#     def _users(self, obj):
#         return ", ".join([item.username for item in obj.users.all()])
#
#     list_display = ('id', 'name', '_users')
#
#
# @admin.register(models.OrganizationMembership)
# class OrganizationMembershipAdmin( admin.ModelAdmin):
#     list_display = ('id', 'user', 'organization')
