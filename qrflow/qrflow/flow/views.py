from django.shortcuts import render, reverse
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

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
        return initial

    def form_valid(self, form):
        data = form.cleaned_data
        print(data)
        return super().form_valid(form)


class CodeDetailView(RelatedOrganizationPermissionMixin, DetailView):
    related_organization_field = "application"
    model = models.Code
