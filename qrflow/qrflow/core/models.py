import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseAbstractModel(models.Model):

    class Meta:
        abstract = True
        ordering = ['-created']

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted = True
        self.save()

    def __str__(self):
        if hasattr(self, "name"):
            return self.name
        else:
            if isinstance(self.id, uuid.UUID):
                return self.id.hex
            return self.id


class CustomUser(AbstractUser, BaseAbstractModel):

    def __str__(self):
        return self.username

#
# class Organization(BaseAbstractModel):
#     name = models.CharField(max_length=128, unique=True)
#     users = models.ManyToManyField("CustomUser", through="OrganizationMembership")
#
#
# class OrganizationMembership(BaseAbstractModel):
#
#     class Meta:
#         unique_together = (('user', 'organization'),)
#
#     user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
#     organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)
#
#
# class OwnershipAbstractModel(models.Model):
#
#     class Meta:
#         abstract = True
#
#     organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)
#     owner = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)

