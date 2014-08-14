import datetime
import unittest
from decimal import Decimal
from formative.registry import FormativeTypeRegistry


class TestSimpleForm(unittest.TestCase):
    def setUp(self):
        SimpleForm = FormativeTypeRegistry().get('simple').form
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        self.obj = f.save(commit=False)

    def test_unique_identifier(self):
        self.assertEqual(self.obj.unique_identifier, 'test-identifier')

    def test_unique_identifier_not_in_data(self):
        self.assertFalse('unique_identifier' in self.obj.data)

    def test_data(self):
        self.assertEqual(self.obj.data['name'], 'test-name')


class TestSimpleFormWithInstance(TestSimpleForm):
    def setUp(self):
        super(TestSimpleFormWithInstance, self).setUp()
        SimpleForm = FormativeTypeRegistry().get('simple').form
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'changed-name'
        }, instance=self.obj)
        f.full_clean()
        self.obj = f.save(commit=False)

    def test_data(self):
        self.assertEqual(self.obj.data['name'], 'changed-name')


class TestFancyForm(unittest.TestCase):
    def setUp(self):
        self.FancyForm = FormativeTypeRegistry().get('fancy').form

    def test_serializes_fancy_form(self):
        f = self.FancyForm({
            'unique_identifier': 'fancy',
            'is_fancy': 'true', 'favorite_color': 'blue',
            'date_of_birth': '1967-05-13', 'income': '1967.05',
            'number_of_fingers': '10', 'family_members': ['mom', 'dad'],
            'time_of_day': '16:20'
        })
        f.full_clean()
        obj = f.save(commit=False)
        self.assertEqual(obj.data, {
            'is_fancy': True,
            'favorite_color': 'blue',
            'date_of_birth': datetime.date(1967, 5, 13),
            'income': Decimal('1967.05'),
            'number_of_fingers': 10,
            'family_members': ['mom', 'dad'],
            'time_of_day': datetime.time(16, 20)
        })
