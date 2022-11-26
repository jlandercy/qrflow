from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from flow import models
from core.permissions import OrganizationPermissionMixin


class ApplicationListView(LoginRequiredMixin, ListView):
    model = models.Application


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = models.Application


class QRCodeView(TemplateView):
    template_name = "flow/qrcode.html"


class ScannerView(TemplateView):
    template_name = "flow/scanner.html"

