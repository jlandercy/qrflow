from django.db import models
from django.core.files.uploadedfile import SimpleUploadedFile

from core.models import BaseAbstractModel, OwnershipAbstractModel
from pki.toolbox import CertificateHelper


class Certificate(BaseAbstractModel, OwnershipAbstractModel):

    def organization_public_path(instance, filename):
        return "organizations/{}/public/{}".format(instance.organization.id.hex, instance.id.hex + ".crt")

    def organization_private_path(instance, filename):
        return "organizations/{}/private/{}".format(instance.organization.id.hex, instance.id.hex + ".key")

    name = models.CharField(max_length=128, unique=True)
    public_key = models.FileField(upload_to=organization_public_path, blank=True)
    private_key = models.FileField(upload_to=organization_private_path, blank=True)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):

        if not(self.public_key and self.private_key):
            # Create new certificates:
            key, cert = CertificateHelper.create_ca()
            print(key, cert)
            self.public_key = SimpleUploadedFile('x', CertificateHelper.to_public_pem(cert))
            self.private_key = SimpleUploadedFile('y', CertificateHelper.to_private_pem(key))
            print(self.public_key)
            print(self.private_key)
