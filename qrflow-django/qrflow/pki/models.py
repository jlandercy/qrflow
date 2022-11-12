import io

from django.db import models
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

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
            public_key = io.BytesIO(CertificateHelper.to_public_pem(cert))
            private_key = io.BytesIO(CertificateHelper.to_private_pem(key))

            self.public_key = InMemoryUploadedFile(public_key, 'FileField', 'ca.crt', 'PEM', public_key.getbuffer().nbytes, None)
            self.private_key = InMemoryUploadedFile(private_key, 'FileField', 'ca.crt', 'PEM', private_key.getbuffer().nbytes, None)

            # Infinite recursion loop, why?
            #self.public_key.save(File(io.BytesIO(CertificateHelper.to_public_pem(cert))))
            #self.private_key.save(File(io.BytesIO(CertificateHelper.to_private_pem(key))))

        super().save()
