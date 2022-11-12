from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    pass
