from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core import models


class OrganizationListView(ListView):
    model = models.Organization

    def get_queryset(self):
        return self.model.objects.filter(id__in=self.request.user.organization_set.all())


class OrganizationDetailView(DetailView):
    model = models.Organization

    def get_queryset(self):
        return self.model.objects.filter(id__in=self.request.user.organization_set.all())

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        response.set_cookie("organization", kwargs["pk"])
        return response

