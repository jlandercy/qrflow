from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from core import models


class OrganizationListView(ListView):
    model = models.Organization


class OrganizationDetailView(DetailView):
    model = models.Organization
