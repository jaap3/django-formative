from django.test import TestCase
from formative.registry import (FormativeType, FormativeTypeRegistry,
                                register, autodiscover)
from tests.testproject.testapp.forms import SimpleForm

autodiscover()


class TestRegistry(TestCase):
    def setUp(self):
        self.registry = FormativeTypeRegistry()

    def test_is_registered(self):
        self.assertTrue('simple' in self.registry)

    def test_get_form(self):
        self.assertEqual(self.registry.get('simple').form, SimpleForm)

    def test_form_has_formative_type_set(self):
        self.assertEqual(self.registry.get('simple').form.formative_type,
                         'simple')

    def test_str(self):
        self.assertEqual(str(self.registry.get('simple')), 'Simple')


class TestRegister(TestCase):
    def test_register(self):
        register('simple-2', SimpleForm)
        self.assertTrue('simple-2' in FormativeTypeRegistry())


class CustomFormativeType(FormativeType):
    def __init__(self, name, form, fieldsets=None, verbose_name=None):
        super(CustomFormativeType, self).__init__(name, form)
        self.verbose_name = 'Custom'


class TestCustomClassRegistry(TestCase):
    def setUp(self):
        register('simple-custom', SimpleForm, cls=CustomFormativeType)
        self.registry = FormativeTypeRegistry()

    def test_is_registered(self):
        self.assertTrue('simple-custom' in FormativeTypeRegistry())

    def test_is_correct_instance(self):
        self.assertIsInstance(self.registry.get('simple-custom'),
                              CustomFormativeType)

    def test_get_form(self):
        self.assertEqual(self.registry.get('simple-custom').form, SimpleForm)

    def test_form_has_formative_type_set(self):
        self.assertEqual(
            self.registry.get('simple-custom').form.formative_type,
            'simple-custom')

    def test_str(self):
        self.assertEqual(str(self.registry.get('simple-custom')),
                         'Custom')
