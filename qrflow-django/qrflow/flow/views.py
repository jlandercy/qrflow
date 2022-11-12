from django.shortcuts import render
from django.views.generic import TemplateView


class QRCodeView(TemplateView):
    template_name = "flow/qrcode.html"


class ScannerView(TemplateView):
    template_name = "flow/scanner.html"
