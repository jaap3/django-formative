from formative.registry import FormativeType, register
from tests.testproject.forms import SimpleForm


register(FormativeType('simple', SimpleForm))
