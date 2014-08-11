from django import forms
from formative.models import FormativeBlob


class FormativeForm(forms.ModelForm):
    formative_type = None

    def save(self, commit=True):
        data = {}
        for key in self.declared_fields.keys():
            data[key] = self[key].value()
        self.instance.formative_type = self.formative_type
        self.instance.data = data
        return super(FormativeForm, self).save(commit=commit)


class FormativeBlobForm(FormativeForm):
    class Meta:
        model = FormativeBlob
        fields = ['unique_identifier']
