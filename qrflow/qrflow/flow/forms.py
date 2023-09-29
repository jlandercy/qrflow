from django import forms


class ApplicationScannerForm(forms.Form):
    organization = forms.CharField(widget=forms.HiddenInput())
    application = forms.CharField(widget=forms.HiddenInput())
    payload = forms.JSONField(required=False, disabled=True, initial=dict())
