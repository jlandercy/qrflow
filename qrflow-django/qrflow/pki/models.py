from django.db import models

from core.models import BaseAbstractModel, OwnershipAbstractModel


class Certificate(BaseAbstractModel, OwnershipAbstractModel):

    def organization_public_directory(instance, filename):
        return "organizations/{}/public/{}".format(instance.organization.id.hex, instance.id.hex + ".crt")

    def organization_private_directory(instance, filename):
        return "organizations/{}/private/{}".format(instance.organization.id.hex, instance.id.hex + ".key")

    public_key = models.FileField(upload_to=organization_public_directory)
    private_key = models.FileField(upload_to=organization_private_directory)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()
        pass

