import base64
import json
from urllib.parse import urlparse

from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from encrypted_json_fields import fields as efields

from qrflow import constants
from core.models import AbstractBaseModel, AbstractOwnershipModel
from flow import managers
from flow.helpers import QRCodeHelper


class Endpoint(AbstractBaseModel, AbstractOwnershipModel):

    class Meta:
        unique_together = ("organization", "name")
        ordering = ("name",)

    name = models.CharField(max_length=128, unique=False)
    method = models.CharField(max_length=8, choices=constants.HTTP_METHODS, default='GET', help_text="HTTP method to contact the endpoint")
    target = models.URLField(help_text="Endpoint target URL (raw or template)")
    parameters = models.JSONField(blank=True, default=dict, help_text="Specific parameters to contact the endpoint (excluded credentials)")
    credentials = efields.EncryptedJSONField(default=dict, null=True, blank=True)

    # def __str__(self):
    #     return "%s: %s %s" % (self.name, self.method, self.target)


class Application(AbstractBaseModel, AbstractOwnershipModel):

    class Meta:
        unique_together = ("organization", "name")
        ordering = ("name",)

    objects = managers.ApplicationManager()
    name = models.CharField(max_length=128, unique=False, help_text="Application name")
    credentials = efields.EncryptedJSONField(default=dict, null=True, blank=True)
    #scanner_mode = models.CharField(max_length=16, choices=constants.SCANNER_MODES, default='RPC', help_text="Scanner mode")
    forward_endpoint = models.ForeignKey(Endpoint, on_delete=models.RESTRICT, null=True, blank=True)
    auto_post = models.BooleanField(default=False)


class Code(AbstractBaseModel):

    class Meta:
        unique_together = ("application", "name")
        ordering = ("zorder", "name")

    def image_path(self, filename):
        return "organizations/{}/applications/{}/codes/{}".format(
            self.application.organization.id.hex,
            self.application.id.hex,
            self.id.hex + ".png"
        )

    application = models.ForeignKey(Application, on_delete=models.RESTRICT, related_name="codes")
    name = models.CharField(max_length=256, unique=False)
    payload = models.JSONField(default=dict, null=True)
    image = models.ImageField(upload_to=image_path, max_length=512, null=False, blank=True)
    zorder = models.IntegerField(default=0)

    @property
    def base64(self):
        return "data:image/png;base64, %s" % base64.b64encode(self.image.read()).decode()

    def save(self, *args, **kwargs):

        image = QRCodeHelper.render(json.dumps(self.payload))

        if self.image:
            self.image.storage.delete(self.image.path)

        self.image = InMemoryUploadedFile(image, 'ImageField', 'qrcode.png', 'PNG', image.getbuffer().nbytes, None)

        super().save(*args, **kwargs)
