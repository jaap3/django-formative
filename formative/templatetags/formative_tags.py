from django import template
from formative.models import FormativeBlob

register = template.Library()


@register.assignment_tag
def get_blob(unique_identifier):
    """
    Get a formative blob by its unique identifier and assign it to a
    template variable.
    """
    try:
        return FormativeBlob.objects.get(unique_identifier=unique_identifier)
    except FormativeBlob.DoesNotExist:
        return None
