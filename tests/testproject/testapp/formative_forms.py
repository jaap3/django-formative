from formative import registry
from tests.testproject.testapp.forms import (SimpleForm, FieldsetForm,
                                             FancyForm, BookRelatedForm)


registry.register('simple', SimpleForm)
registry.register('fieldset-identifier', FieldsetForm, [
    (None, {'fields': ['unique_identifier']}),
    ('Title', {'fields': ['title']}),
    ('Body', {'fields': ['body']})
])
registry.register('fieldset-no-identifier', FieldsetForm, [
    ('Title', {'fields': ['title']}),
    ('Body', {'fields': ['body']})
])
registry.register('fancy', FancyForm)
registry.register('related', BookRelatedForm)
