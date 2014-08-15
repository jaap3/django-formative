import formative
from tests.testproject.testapp.forms import (SimpleForm, FieldsetForm,
                                             FancyForm, BookRelatedForm)


formative.register('simple', SimpleForm)
formative.register('fieldset-identifier', FieldsetForm, [
    (None, {'fields': ['unique_identifier']}),
    ('Title', {'fields': ['title']}),
    ('Body', {'fields': ['body']})
])
formative.register('fieldset-no-identifier', FieldsetForm, [
    ('Title', {'fields': ['title']}),
    ('Body', {'fields': ['body']})
])
formative.register('fancy', FancyForm)
formative.register('related', BookRelatedForm)
