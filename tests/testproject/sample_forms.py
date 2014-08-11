from django import forms
from formative.forms import FormativeForm


class SimpleForm(FormativeForm):
    name = forms.CharField()
