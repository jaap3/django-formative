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
        self.assertEqual(
            registry.get('simple').form.formative_type, registry['simple'])

    def test_str(self):
        self.assertEqual(str(registry.get('simple')), 'Simple')

    def test_len(self):
        self.assertEqual(len(registry), 7)


class TestRegisterSameFormTwice(TestCase):
    def setUp(self):
        register('simple-2', SimpleForm)

    def test_in_registry(self):
        self.assertTrue('simple-2' in registry)

    def test_type_is_set_correctly(self):
        self.assertEqual(
            registry['simple-2'].form.formative_type, registry['simple-2'])

    def test_type_is_set_correctly_for_other_type(self):
        self.assertEqual(
            registry['simple'].form.formative_type, registry['simple'])


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
        self.assertIsInstance(
            registry.get('simple-custom').form.formative_type,
            CustomFormativeType)

    def test_str(self):
        self.assertEqual(str(registry.get('simple-custom')), 'Custom')
