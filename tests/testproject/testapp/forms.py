from django import forms
from formative.forms import FormativeBlobForm


class SimpleForm(FormativeBlobForm):
    name = forms.CharField()


class FieldsetForm(FormativeBlobForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
