from django import forms
from formative.forms import FormativeBlobForm


class SimpleForm(FormativeBlobForm):
    formative_type = 'simple'
    name = forms.CharField()
