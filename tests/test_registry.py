import unittest

from formative.registry import FormativeTypeRegistry
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
