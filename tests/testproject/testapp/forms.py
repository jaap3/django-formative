from django import forms
from formative.forms import FormativeForm
from django.forms.extras import SelectDateWidget
from tests.testproject.testapp.models import Book


class SimpleForm(FormativeForm):
    name = forms.CharField()


class FieldsetForm(FormativeForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)


class FancyForm(FormativeForm):
    is_fancy = forms.BooleanField(initial=True, required=False)
    favorite_color = forms.ChoiceField(choices=[
        ('red', 'Red'), ('geen', 'Green'), ('blue', 'Blue')])
    date_of_birth = forms.DateField(widget=SelectDateWidget, required=False)
    income = forms.DecimalField()
    number_of_fingers = forms.IntegerField(initial=10)
    family_members = forms.MultipleChoiceField(choices=[
        ('mom', 'Mom'), ('dad', 'Dad'),
        ('brothers', 'Brother(s)'), ('sisters', 'Sister(s)')])
    time_of_day = forms.TimeField()


class BookRelatedForm(FormativeForm):
    book = forms.ModelChoiceField(queryset=Book.objects.all())
