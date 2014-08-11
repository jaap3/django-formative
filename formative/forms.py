from django import forms
from formative.models import FormBlob


class FormativeForm(forms.ModelForm):
    class Meta:
        model = FormBlob
        fields = ['unique_identifier']

    def save(self, commit=True):
        data = {}
        for key in self.declared_fields.keys():
            data[key] = self[key].value()
        self.instance.data = data
        return super(FormativeForm, self).save(commit=commit)
