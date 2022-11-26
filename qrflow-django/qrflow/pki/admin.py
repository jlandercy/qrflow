from django.contrib import admin

from core.admin import OrganizationAdminMixin
from pki import models


@admin.register(models.Certificate)
class CertificateAdmin(OrganizationAdminMixin, admin.ModelAdmin):

    def _signature(self, obj):
        return obj.signature[:32]

    def _subject(self, obj):
        return obj.subject

    list_display = ('id', 'organization', 'owner', 'name', '_signature', '_subject', 'public_key', 'private_key')

