from django.urls import path, include

from flow import views


app_name = 'flow'

urlpatterns = [

    path(r"application/<uuid:pk>/", views.ApplicationDetailView.as_view(), name="application-detail"),
    path(r"application/<uuid:pk>/scanner/", views.ApplicationScannerView.as_view(), name="application-scanner"),

    path(r"code/<uuid:pk>/", views.CodeDetailView.as_view(), name="code-detail"),

]
