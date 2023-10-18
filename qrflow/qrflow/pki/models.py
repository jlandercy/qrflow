import io

from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile

from cryptography import x509

from core.models import AbstractBaseModel, AbstractOwnershipModel
from pki.helpers import CertificateHelper


class Certificate(AbstractBaseModel, AbstractOwnershipModel):

    def organization_public_path(self, filename):
        return "organizations/{}/certificates/public/{}".format(self.organization.id.hex, self.id.hex + ".crt")

    def organization_private_path(self, filename):
        return "organizations/{}/certificates/private/{}".format(self.organization.id.hex, self.id.hex + ".key")

    name = models.CharField(max_length=128, unique=True)
    public_key = models.FileField(upload_to=organization_public_path, null=False, blank=True)
    private_key = models.FileField(upload_to=organization_private_path, null=False, blank=True)

    @property
    def signature(self):
        with self.public_key.open("rb") as handler:
            return x509.load_pem_x509_certificate(handler.read()).signature.hex()

    @property
    def subject(self):
        with self.public_key.open("rb") as handler:
            return x509.load_pem_x509_certificate(handler.read()).subject.rfc4514_string()

    def save(self, *args, **kwargs):

        if not(self.public_key and self.private_key):

            # Create new CA Certificate:
            key, cert = CertificateHelper.create_ca()
            public_key = io.BytesIO(CertificateHelper.to_public_pem(cert))
            private_key = io.BytesIO(CertificateHelper.to_private_pem(key))

            # Bind PEM Files:
            self.public_key = InMemoryUploadedFile(
                public_key, 'FileField', 'ca.crt', 'PEM', public_key.getbuffer().nbytes, None
            )
            self.private_key = InMemoryUploadedFile(
                private_key, 'FileField', 'ca.key', 'PEM', private_key.getbuffer().nbytes, None
            )

        super().save(*args, **kwargs)
