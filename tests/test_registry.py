import unittest

from formative.registry import FormativeTypeChoices
from tests.testproject.testapp.forms import SimpleForm


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.choices = FormativeTypeChoices()

    def test_is_registered(self):
        self.assertTrue('simple' in self.choices)

    def test_get_form(self):
        self.assertEqual(self.choices['simple'].get_form(), SimpleForm)
