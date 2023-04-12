from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core import models
from core.permissions import OrganizationPermissionMixin, OrganizationMembershipPermissionMixin


class OrganizationListView(OrganizationPermissionMixin, ListView):
    model = models.Organization


class OrganizationDetailView(OrganizationMembershipPermissionMixin, DetailView):
    model = models.Organization
