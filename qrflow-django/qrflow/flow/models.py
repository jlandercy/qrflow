import io

from django.db import models
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.models import BaseAbstractModel, OwnershipAbstractModel
from flow.helpers import QRCodeHelper


class Application(BaseAbstractModel, OwnershipAbstractModel):

    name = models.CharField(max_length=128, unique=True)
    # Integration + Credentials
    target = models.URLField()


class Code(BaseAbstractModel):

    def image_path(self, filename):
        return "organizations/{}/applications/{}/codes/{}".format(
            self.application.organization.id.hex,
            self.application.id.hex,
            self.id.hex + ".png"
        )

    application = models.ForeignKey(Application, on_delete=models.RESTRICT)
    name = models.CharField(max_length=1024, unique=True)
    payload = models.JSONField()
    image = models.ImageField(upload_to=image_path, max_length=512, null=False, blank=True)

    def save(self):

        if "payload" in self.payload:
            image = QRCodeHelper.render(self.payload["payload"])
        else:
            image = QRCodeHelper.render(self.payload)
        self.image = InMemoryUploadedFile(image, 'ImageField', 'qrcode.png', 'PNG', image.getbuffer().nbytes, None)

        super().save()
