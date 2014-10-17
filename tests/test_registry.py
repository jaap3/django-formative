from django.test import TestCase
from formative import autodiscover
from formative.models import FormativeBlob, InlineFormativeBlob
from formative.registry import FormativeType
from tests.testproject.testapp.forms import SimpleForm

autodiscover()


class CustomFormativeType(FormativeType):
    name = 'simple-custom'
    form_class = SimpleForm
    verbose_name = 'Custom'


class ReuseFormType(FormativeType):
    name = 'simple-2'
    form_class = SimpleForm


class TestFormativeBlobRegistry(TestCase):
    blob_cls = FormativeBlob

    def test_is_registered(self):
        self.assertTrue('simple' in self.blob_cls.registry)

    def test_form(self):
        self.assertTrue(issubclass(
            self.blob_cls.registry.get('simple').form, SimpleForm))

    def test_form_has_formative_type_set(self):
        self.assertEqual(
            self.blob_cls.registry.get('simple').form.formative_type,
            self.blob_cls.registry.get('simple'))

    def test_str(self):
        self.assertEqual(
            str(self.blob_cls.registry.get('simple')), 'Simple')

    def test_len(self):
        self.assertEqual(len(FormativeBlob.registry), 6)


class TestInlineFormativeBlobRegistry(TestCase):
    blob_cls = InlineFormativeBlob

    def test_len(self):
        self.assertEqual(len(InlineFormativeBlob.registry), 2)


class TestCustomClassRegistry(TestCase):
    def setUp(self):
        FormativeBlob.register(CustomFormativeType)

    def test_is_registered(self):
        self.assertTrue('simple-custom' in FormativeBlob.registry)

    def test_is_correct_instance(self):
        self.assertIsInstance(
            FormativeBlob.registry.get('simple-custom'), CustomFormativeType)

    def test_form(self):
        self.assertTrue(issubclass(
            FormativeBlob.registry.get('simple-custom').form, SimpleForm))

    def test_form_has_formative_type_set(self):
        self.assertIsInstance(
            FormativeBlob.registry.get('simple-custom').form.formative_type,
            CustomFormativeType)

    def test_str(self):
        self.assertEqual(
            str(FormativeBlob.registry.get('simple-custom')), 'Custom')


class TestRegisterSameFormTwice(TestCase):
    def setUp(self):
        FormativeBlob.register(ReuseFormType)

    def test_in_registry(self):
        self.assertTrue('simple-2' in FormativeBlob.registry)

    def test_type_is_set_correctly(self):
        self.assertEqual(
            FormativeBlob.registry.get('simple-2').form.formative_type,
            FormativeBlob.registry.get('simple-2'))

    def test_type_is_set_correctly_for_other_type(self):
        self.assertEqual(
            FormativeBlob.registry.get('simple-custom').form.formative_type,
            FormativeBlob.registry.get('simple-custom'))
