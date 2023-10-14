from django import forms


class ApplicationScannerForm(forms.Form):
    organization = forms.CharField(widget=forms.HiddenInput())
    application = forms.CharField(widget=forms.HiddenInput())
    repeat_scan = forms.BooleanField(required=False, disabled=False)
    scan_delay = forms.FloatField(required=False, disabled=False)
    auto_post = forms.BooleanField(required=False, disabled=False)
    payload = forms.JSONField(required=False, disabled=False, initial=dict)
