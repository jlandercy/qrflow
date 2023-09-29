from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.permissions import OrganizationPermissionMixin, RelatedOrganizationPermissionMixin
from flow import models, forms


class ApplicationListView(OrganizationPermissionMixin, ListView):
    model = models.Application


class ApplicationDetailView(OrganizationPermissionMixin, DetailView):
    model = models.Application

    # def get(self, request, *args, **kwargs):
    #     response = super().get(self, request, *args, **kwargs)
    #     response.set_cookie("application", kwargs["pk"])
    #     return response


class ApplicationScannerView(FormView):
    template_name = "flow/application_scanner.html"
    model = models.Application
    form_class = forms.ApplicationScannerForm

    def get_success_url(self):
        return reverse('flow:application-scanner', kwargs={'pk': self.kwargs["pk"]})


class CodeDetailView(RelatedOrganizationPermissionMixin, DetailView):
    related_organization_field = "application"
    model = models.Code


class QRCodeView(TemplateView):
    template_name = "flow/qrcode.html"


class ScannerView(TemplateView):
    template_name = "flow/scanner.html"

