from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static, serve

from core import views


app_name = 'core'

urlpatterns = [
    path(r"organization/", views.OrganizationListView.as_view(), name="organization-list"),
    path(r"organization/<uuid:pk>/", views.OrganizationDetailView.as_view(), name="organization-detail"),
]
