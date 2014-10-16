from formative.forms import FormativeTypeForm


def get_type_from_request(request):
    """
    Get formative type from request
    """
    form = FormativeTypeForm(request.GET)
    if form.is_valid():
        return form.cleaned_data['formative_type']
    return None
