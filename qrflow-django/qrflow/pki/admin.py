from django.contrib import admin

from pki import models


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'owner', 'name', 'public_key', 'private_key')

