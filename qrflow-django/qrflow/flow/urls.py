from django.conf import settings
from django.urls import path, re_path, include
from django.conf.urls.static import static, serve

from flow import views


app_name = 'flow'

urlpatterns = [
    path(r"qrcode", views.QRCodeView.as_view(), name="qrcode"),
    path(r"scanner", views.ScannerView.as_view(), name="scanner"),
]
