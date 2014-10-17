from formative.models import FormativeBlob, InlineFormativeBlob
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
    fieldsets = [
        (None, {'fields': ['is_fancy']}),
        ('Dates & Time', {'fields': ['date_of_birth', 'time_of_day']}),
        ('Numbers', {'fields': ['number_of_fingers', 'income']}),
        ('Selects', {'fields': ['favorite_color', 'family_members']}),
    ]


class RelatedType(FormativeType):
    name = 'related'
    form_class = BookRelatedForm


FormativeBlob.register(
    SimpleType, FieldsetIdentifier,
    FieldsetNoIdentifier, FancyType, RelatedType)

InlineFormativeBlob.register(SimpleType, FancyType)
