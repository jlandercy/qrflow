import io
import base64
from urllib.parse import urlparse

from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from core.models import AbstractBaseModel, AbstractOwnershipModel
from flow import managers
from flow.helpers import QRCodeHelper


class Application(AbstractBaseModel, AbstractOwnershipModel):

    objects = managers.ApplicationManager()
    name = models.CharField(max_length=128, unique=True, help_text="Application name")
    domain = models.URLField(help_text="Domain to validate endpoint URLs")


class Endpoint(AbstractBaseModel):

    application = models.ForeignKey(Application, on_delete=models.RESTRICT, help_text="Endpoint's application")
    name = models.CharField(max_length=128, unique=True)
    target = models.URLField(help_text="Endpoint target URL (raw or template)")

    def clean(self):
        url = urlparse(self.target)
        if url.hostname != self.application.domain:
            raise ValidationError(
                'Application endpoint %s must belong to application domain %s' %
                (self.target, self.application.domain)
            )


class Code(AbstractBaseModel):

    class Meta:
        ordering = ("zorder", "name")

    def image_path(self, filename):
        return "organizations/{}/applications/{}/codes/{}".format(
            self.application.organization.id.hex,
            self.application.id.hex,
            self.id.hex + ".png"
        )

    application = models.ForeignKey(Application, on_delete=models.RESTRICT, related_name="codes")
    name = models.CharField(max_length=1024, unique=True)
    payload = models.JSONField()
    image = models.ImageField(upload_to=image_path, max_length=512, null=False, blank=True)
    zorder = models.IntegerField(default=0)

    @property
    def base64(self):
        return "data:image/png;base64, %s" % base64.b64encode(self.image.read()).decode()

    def save(self, *args, **kwargs):

        if "payload" in self.payload:
            image = QRCodeHelper.render(self.payload["payload"])
        else:
            image = QRCodeHelper.render(self.payload)
        self.image = InMemoryUploadedFile(image, 'ImageField', 'qrcode.png', 'PNG', image.getbuffer().nbytes, None)

        super().save(*args, **kwargs)
