from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from organizations.views.mixins import MembershipRequiredMixin, OrganizationMixin

from flow import models


class ApplicationListView(LoginRequiredMixin, ListView):
    model = models.Application


class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = models.Application


class CodeDetailView(DetailView):
    model = models.Code


class QRCodeView(TemplateView):
    template_name = "flow/qrcode.html"


class ScannerView(TemplateView):
    template_name = "flow/scanner.html"

