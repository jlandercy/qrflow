from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

import requests

from core.permissions import OrganizationPermissionMixin, RelatedOrganizationPermissionMixin
from flow import models, forms


class ApplicationDetailView(OrganizationPermissionMixin, DetailView):
    model = models.Application

    # def get(self, request, *args, **kwargs):
    #     response = super().get(self, request, *args, **kwargs)
    #     response.set_cookie("application", kwargs["pk"])
    #     return response


class ApplicationScannerView(DetailView, FormView):
    template_name = "flow/application_scanner.html"
    model = models.Application
    form_class = forms.ApplicationScannerForm

    def get_success_url(self):
        return reverse('flow:application-scanner', kwargs={'pk': self.kwargs["pk"]})

    def get_initial(self):
        initial = super().get_initial()
        application = models.Application.objects.get(pk=self.kwargs['pk'])
        initial['organization'] = application.organization.id
        initial['application'] = application.id
        initial['auto_post'] = application.auto_post
        return initial

    def form_valid(self, form):

        application = models.Application.objects.get(pk=self.kwargs['pk'])

        if application.forward_endpoint:
            try:
                response = requests.request(
                    application.forward_endpoint.method,
                    url=application.forward_endpoint.target,
                    headers={},
                    json=form.cleaned_data
                )
                messages.info(self.request, response.json())
            except Exception as error:
                messages.error(self.request, str(error))

        return super().form_valid(form)


class CodeDetailView(RelatedOrganizationPermissionMixin, DetailView):
    related_organization_field = "application"
    model = models.Code
