import unittest

from formative.registry import FormativeType, FormativeTypeRegistry, register
from tests.testproject.testapp.forms import SimpleForm


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = FormativeTypeRegistry()

    def test_is_registered(self):
        self.assertTrue('simple' in self.registry)

    def test_get_form(self):
        self.assertEqual(self.registry.get('simple').form, SimpleForm)

    def test_form_has_formative_type_set(self):
        self.assertEqual(self.registry.get('simple').form.formative_type,
                         'simple')

    def test_unicode(self):
        self.assertEqual(unicode(self.registry.get('simple')), 'Simple')


class TestRegister(unittest.TestCase):
    def test_register(self):
        register(FormativeType('simple-2', SimpleForm))
        self.assertTrue('simple-2' in FormativeTypeRegistry())


class CustomFormativeType(FormativeType):
    def __init__(self):
        super(CustomFormativeType, self).__init__('simple-custom', SimpleForm)
        self.verbose_name = 'Custom'


class TestCustomClassRegistry(unittest.TestCase):
    def setUp(self):
        register(CustomFormativeType())
        self.registry = FormativeTypeRegistry()

    def test_is_registered(self):
        self.assertTrue('simple-custom' in FormativeTypeRegistry())

    def test_get_form(self):
        self.assertEqual(self.registry.get('simple-custom').form, SimpleForm)

    def test_form_has_formative_type_set(self):
        self.assertEqual(
            self.registry.get('simple-custom').form.formative_type,
            'simple-custom')

    def test_unicode(self):
        self.assertEqual(unicode(self.registry.get('simple-custom')),
                         'Custom')
