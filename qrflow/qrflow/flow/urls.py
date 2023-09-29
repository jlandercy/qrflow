from django.urls import path, include

from flow import views


app_name = 'flow'

urlpatterns = [

    path(r"qrcode/", views.QRCodeView.as_view(), name="qrcode"),
    path(r"scanner/", views.ScannerView.as_view(), name="scanner"),

    path(r"application/", views.ApplicationListView.as_view(), name="application-list"),
    path(r"application/<uuid:pk>/", views.ApplicationDetailView.as_view(), name="application-detail"),
    path(r"application/<uuid:pk>/scanner/", views.ApplicationScannerView.as_view(), name="application-scanner"),

    path(r"code/<uuid:pk>/", views.CodeDetailView.as_view(), name="code-detail"),

]
