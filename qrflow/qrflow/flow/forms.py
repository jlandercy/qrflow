from django import forms


class ApplicationScannerForm(forms.Form):
    organization = forms.CharField(widget=forms.HiddenInput())
    application = forms.CharField(widget=forms.HiddenInput())
    auto_post = forms.BooleanField(required=False)
    payload = forms.JSONField(required=False, disabled=False, initial=dict)
