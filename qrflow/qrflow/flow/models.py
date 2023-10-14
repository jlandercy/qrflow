import base64
import json
from urllib.parse import urlparse

import barcode
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

from encrypted_json_fields import fields as efields

from qrflow import constants
from core.models import AbstractBaseModel, AbstractOwnershipModel
from flow import managers
from flow.helpers import QRCodeHelper, DigitalGreenCertificateHelper, EPCHelper, BarcodeHelper


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
    repeat_scan = models.BooleanField(default=False, null=False)
    auto_post = models.BooleanField(default=False, null=False)
    scan_delay = models.FloatField(default=0., null=False)


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
    code_type = models.CharField(max_length=16, choices=constants.CODE_TYPES, default='QR', help_text="Type of code")
    name = models.CharField(max_length=256, unique=False)
    payload = models.JSONField(default=dict, null=True, blank=True)
    image = models.ImageField(upload_to=image_path, max_length=512, null=False, blank=True)
    zorder = models.IntegerField(default=0)

    @property
    def base64(self):
        return "data:image/png;base64, %s" % base64.b64encode(self.image.read()).decode()

    def save(self, *args, **kwargs):

        if self.code_type == "QR":
            image = QRCodeHelper.render(self.payload["message"])
        elif self.code_type == "QR-JSON":
            image = QRCodeHelper.render(json.dumps(self.payload))
        elif self.code_type == "QR-EPC":
            image = QRCodeHelper.render(EPCHelper.encode(**self.payload))
        elif self.code_type == "QR-DGC":
            image = QRCodeHelper.render(DigitalGreenCertificateHelper.encode(self.payload))
        elif self.code_type in barcode.PROVIDED_BARCODES:
            image = BarcodeHelper.render(self.payload["message"], class_name=self.code_type)
        else:
            image = QRCodeHelper.render("Not implemented :(")

        if self.image:
            self.image.storage.delete(self.image.path)

        self.image = InMemoryUploadedFile(image, 'ImageField', 'code.png', 'PNG', image.getbuffer().nbytes, None)

        super().save(*args, **kwargs)


class Log(AbstractBaseModel):

    class Meta:
        ordering = ("-created",)

    application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, blank=True)
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(null=True, blank=False)
    payload = models.JSONField(null=True, blank=False)
    response = models.JSONField(null=True, blank=False)
