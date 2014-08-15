from django import forms
from formative.forms import FormativeBlobForm
from django.forms.extras import SelectDateWidget
from tests.testproject.testapp.models import Book


class SimpleForm(FormativeBlobForm):
    name = forms.CharField()


class FieldsetForm(FormativeBlobForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)


class FancyForm(FormativeBlobForm):
    is_fancy = forms.BooleanField(initial=True, required=False)
    favorite_color = forms.ChoiceField(choices=[
        ('red', 'Red'), ('geen', 'Green'), ('blue', 'Blue')])
    date_of_birth = forms.DateField(widget=SelectDateWidget)
    income = forms.DecimalField()
    number_of_fingers = forms.IntegerField(initial=10)
    family_members = forms.MultipleChoiceField(choices=[
        ('mom', 'Mom'), ('dad', 'Dad'),
        ('brothers', 'Brother(s)'), ('sisters', 'Sister(s)')])
    time_of_day = forms.TimeField()


class BookRelatedForm(FormativeBlobForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
