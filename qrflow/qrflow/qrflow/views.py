from django.shortcuts import redirect
from django.conf import settings
from django.views import View
from django.views.static import serve
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


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

    def get(self, request, path, *args, **kwargs):
        return serve(request, path, document_root=settings.MEDIA_ROOT)
