from django.db import models
from django.db.models import F, Count


class ApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            code_count=Count(F("codes__id"), distinct=True)
        )


class CodeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
