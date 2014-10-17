from formative.models import FormativeBlob
from formative.registry import FormativeType
from tests.testproject.testapp.forms import (
    SimpleForm, FieldsetForm, FancyForm, BookRelatedForm)


class SimpleType(FormativeType):
    name = 'simple'
    form_class = SimpleForm


class FieldsetIdentifier(FormativeType):
    name = 'fieldset-identifier'
    form_class = FieldsetForm
    fieldsets = [
        (None, {'fields': ['unique_identifier']}),
        ('Title', {'fields': ['title']}),
        ('Body', {'fields': ['body']})
    ]


class FieldsetNoIdentifier(FormativeType):
    name = 'fieldset-no-identifier'
    form_class = FieldsetForm
    fieldsets = [
        ('Title', {'fields': ['title']}),
        ('Body', {'fields': ['body']})
    ]


class FancyType(FormativeType):
    name = 'fancy'
    form_class = FancyForm


class RelatedType(FormativeType):
    name = 'related'
    form_class = BookRelatedForm


FormativeBlob.register(
    SimpleType, FieldsetIdentifier,
    FieldsetNoIdentifier, FancyType, RelatedType
)
