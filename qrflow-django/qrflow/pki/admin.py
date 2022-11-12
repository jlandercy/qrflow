from django.contrib import admin

from pki import models


@admin.register(models.Certificate)
class CertificateAdmin(admin.ModelAdmin):
    pass

