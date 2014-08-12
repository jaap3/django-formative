from django import forms
from formative.forms import FormativeBlobForm


class SimpleForm(FormativeBlobForm):
    name = forms.CharField()
