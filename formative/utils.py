from django.forms.models import modelform_factory


def formative_form_factory(model, form, exclude=None):
    exclude = exclude or []
    exclude.extend(['formative_type', 'json_data'])
    return modelform_factory(
        model, form=form, exclude=exclude)
