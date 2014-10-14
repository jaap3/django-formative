from django.test import TestCase
from formative import registry, register, autodiscover
from formative.registry import FormativeType
from tests.testproject.testapp.forms import SimpleForm

autodiscover()


class TestRegistry(TestCase):
    def test_is_registered(self):
        self.assertTrue('simple' in registry)

    def test_get_form(self):
        self.assertEqual(registry.get('simple').form, SimpleForm)

    def test_form_has_formative_type_set(self):
        self.assertEqual(registry.get('simple').form.formative_type, 'simple')

    def test_str(self):
        self.assertEqual(str(registry.get('simple')), 'Simple')

    def test_len(self):
        self.assertEqual(len(registry), 11)


class TestRegister(TestCase):
    def test_register(self):
        register('simple-2', SimpleForm)
        self.assertTrue('simple-2' in registry)


class CustomFormativeType(FormativeType):
    def __init__(self, name, form, fieldsets=None, verbose_name=None):
        super(CustomFormativeType, self).__init__(name, form)
        self.verbose_name = 'Custom'


class TestCustomClassRegistry(TestCase):
    def setUp(self):
        register('simple-custom', SimpleForm, cls=CustomFormativeType)

    def test_is_registered(self):
        self.assertTrue('simple-custom' in registry)

    def test_is_correct_instance(self):
        self.assertIsInstance(
            registry.get('simple-custom'), CustomFormativeType)

    def test_get_form(self):
        self.assertEqual(registry.get('simple-custom').form, SimpleForm)

    def test_form_has_formative_type_set(self):
        self.assertEqual(registry.get('simple-custom').form.formative_type,
                         'simple-custom')

    def test_str(self):
        self.assertEqual(str(registry.get('simple-custom')), 'Custom')
