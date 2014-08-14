from formative.registry import FormativeType, register
from tests.testproject.testapp.forms import SimpleForm, FieldsetForm


register(FormativeType('simple', SimpleForm))
register(FormativeType('fieldset-identifier', FieldsetForm, [
    (None, {'fields': ['unique_identifier']}),
    ('Title', {'fields': ['title']}),
    ('Body', {'fields': ['body']})
]))
register(FormativeType('fieldset-no-identifier', FieldsetForm, [
    ('Title', {'fields': ['title']}),
    ('Body', {'fields': ['body']})
]))
