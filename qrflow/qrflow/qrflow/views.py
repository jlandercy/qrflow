from django.shortcuts import redirect
from django.conf import settings
from django.views import View
from django.views.static import serve
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound

from core.models import Organization
from flow.models import Code
from pki.models import Certificate


class ProjectHomeView(TemplateView):

    template_name = "qrflow/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get(self, request, *args, **kwargs):
    #     return redirect("index")


class ProfileView(LoginRequiredMixin, TemplateView):

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get(self, request, *args, **kwargs):
    #     return redirect("index")


class FileServerView(LoginRequiredMixin, View):

    @staticmethod
    def get_file_list(request):
        organization = Organization.objects.get(id=request.COOKIES["organization"])
        files = set()
        files.update(Code.objects.filter(application__organization=organization).values_list("image", flat=True))
        files.update(Certificate.objects.filter(organization=organization).values_list("public_key", flat=True))
        return files

    def get(self, request, path, *args, **kwargs):
        files = self.get_file_list(request)
        if path in files:
            return serve(request, path, document_root=settings.MEDIA_ROOT)
        else:
            return HttpResponseNotFound("File not found")
