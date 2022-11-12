import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseAbstractModel(models.Model):

    class Meta:
        abstract = True
        ordering = ['-created_at']

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    deleted = models.BooleanField(default=False)

    def soft_delete(self):
        self.deleted = True
        self.save()


class CustomUser(AbstractUser, BaseAbstractModel):

    def __str__(self):
        return self.username

