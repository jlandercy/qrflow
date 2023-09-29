from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.permissions import OrganizationPermissionMixin, RelatedOrganizationPermissionMixin
from flow import models


class ApplicationListView(OrganizationPermissionMixin, ListView):
    model = models.Application


class ApplicationDetailView(OrganizationPermissionMixin, DetailView):
    model = models.Application

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        response.set_cookie("application", kwargs["pk"])
        return response


class CodeDetailView(RelatedOrganizationPermissionMixin, DetailView):
    related_organization_field = "application"
    model = models.Code


class QRCodeView(TemplateView):
    template_name = "flow/qrcode.html"


class ScannerView(TemplateView):
    template_name = "flow/scanner.html"

