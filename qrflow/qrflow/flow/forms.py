from django import forms


class ApplicationScannerForm(forms.Form):
    payload = forms.JSONField()
