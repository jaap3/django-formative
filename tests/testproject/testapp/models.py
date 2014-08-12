from formative.registry import FormativeType, register
from tests.testproject.testapp.forms import SimpleForm


register(FormativeType('simple', SimpleForm))
