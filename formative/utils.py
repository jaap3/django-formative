from copy import deepcopy
from django.forms.models import modelform_factory


def formative_form_factory(model, form, exclude=None):
    # prevent recursive import
    from formative.fields import HiddenFormativeTypeInput
    exclude = exclude or []
    exclude.extend(['json_data'])
    return modelform_factory(
        model, form=form, exclude=exclude, widgets={
            'formative_type': HiddenFormativeTypeInput
        })


def add_field_to_fieldsets(field_name, fieldsets):
    """
    Force a field to be in a fieldsets definition.
    """
    # First check if the field is already in there
    for label, fieldset in fieldsets:
        if field_name in fieldset['fields']:
            return fieldsets  # We found it!
    # Didn't find it. Deepcopy the definition so we don't modify it in place!
    fieldsets = deepcopy(list(fieldsets))
    # Try to add it to the first unlabeled fieldset
    for label, fieldset in fieldsets:
        if label is None:
            fieldset['fields'] = [field_name] + list(fieldset['fields'])
            return fieldsets  # We've added it
    # Just add it by itself, as a unlabeled fieldset
    return [(None, {'fields': [field_name]})] + fieldsets
