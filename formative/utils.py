from django.forms.models import modelform_factory
from formative.forms import FormativeTypeForm


def formative_form_factory(model, form):
    return modelform_factory(
        model, form=form, exclude=['formative_type', 'json_data'])


def get_type_from_request(request):
    """
    Get formative type from request
    """
    form = FormativeTypeForm(request.GET)
    if form.is_valid():
        return form.cleaned_data['formative_type']
    return None
