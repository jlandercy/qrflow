from django.db import models

from core.models import BaseAbstractModel, OwnershipAbstractModel


class Certificate(BaseAbstractModel, OwnershipAbstractModel):

    public_key = models.FileField(upload_to='organizations/org/public')
    private_key = models.FileField(upload_to='organizations/org/private')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()
        pass
    
