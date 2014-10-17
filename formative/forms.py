from django import forms


class FormativeTypeForm(forms.ModelForm):
    """
    Select a type
    """
    class Meta:
        fields = ['formative_type']


class FormativeForm(forms.ModelForm):
    """
    Base form for all formative type forms
    """
    formative_type = None  # Gets set by registering a form with a type

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        initial = kwargs.pop('initial', None)
        if instance:
            # Restore form data from instance
            data = instance.data.copy()
            if initial is not None:
                data.update(initial)
            initial = data
        super(FormativeForm, self).__init__(
            instance=instance, initial=initial, *args, **kwargs)

    def save(self, commit=True):
        # Store all non-model data as json
        data = {}
        for key in self.declared_fields.keys():
            data[key] = self[key].value()
        self.instance.formative_type = self.formative_type
        self.instance.data = data
        return super(FormativeForm, self).save(commit=commit)
