from django.forms.models import modelform_factory


def formative_form_factory(model, form):
    return modelform_factory(
        model, form=form, exclude=['formative_type', 'json_data'])
