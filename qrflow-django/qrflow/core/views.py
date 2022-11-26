from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core import models
from core.permissions import OrganizationPermissionMixin


class OrganizationListView(OrganizationPermissionMixin, ListView):
    model = models.Organization


class OrganizationDetailView(OrganizationPermissionMixin, DetailView):
    model = models.Organization