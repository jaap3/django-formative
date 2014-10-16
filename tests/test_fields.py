from unittest import TestCase
from django.core.exceptions import ValidationError
from django.forms import Select
from formative import registry
from formative.fields import FormativeTypeField


class TestFormativeTypeField(TestCase):
    def setUp(self):
        self.field = FormativeTypeField()

    def test_widget_is_select(self):
        self.assertIsInstance(self.field.widget, Select)

    def test_widget_choices(self):
        self.assertEqual(
            list(self.field.widget.choices), list(sorted(registry.items())))

    def test_clean_valid(self):
        self.assertEqual(self.field.clean('simple'), registry['simple'])

    def test_clean_invalid(self):
        with self.assertRaises(ValidationError) as e:
            self.field.clean('invalid')
        self.assertEqual(
            e.exception.messages,
            ['Select a valid type. invalid is not a known type.'])
