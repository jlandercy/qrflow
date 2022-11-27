from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from flow import models
from core.permissions import OrganizationPermissionMixin
from flow.permissions import ApplicationPermissionMixin


class ApplicationListView(OrganizationPermissionMixin, ListView):
    model = models.Application


class ApplicationDetailView(OrganizationPermissionMixin, DetailView):
    model = models.Application


class CodeDetailView(ApplicationPermissionMixin, DetailView):
    model = models.Code


class QRCodeView(TemplateView):
    template_name = "flow/qrcode.html"


class ScannerView(TemplateView):
    template_name = "flow/scanner.html"

