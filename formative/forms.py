from django import forms
from formative.fields import FormativeTypeField
from formative.models import FormativeBlob


class FormativeTypeForm(forms.Form):
    formative_type = FormativeTypeField()


class FormativeForm(forms.ModelForm):
    formative_type = None

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        initial = kwargs.pop('initial', None)
        if instance:
            data = instance.data.copy()
            if initial is not None:
                data.update(initial)
            initial = data
        super(FormativeForm, self).__init__(
            instance=instance, initial=initial, *args, **kwargs)

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
