import unittest
from formative.registry import FormativeType, FormativeTypeChoices, register
from tests.testproject.forms import SimpleForm


class TestRegistry(unittest.TestCase):
    def setUp(self):
        register(FormativeType('simple', SimpleForm))
        self.choices = FormativeTypeChoices()

    def test_is_registered(self):
        self.assertTrue('simple' in self.choices)

    def test_get_form(self):
        self.assertEqual(self.choices['simple'].get_form(), SimpleForm)
