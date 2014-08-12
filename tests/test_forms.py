import unittest
from formative.registry import FormativeTypeRegistry


class TestSimpleForm(unittest.TestCase):
    def setUp(self):
        SimpleForm = FormativeTypeRegistry().get('simple').get_form()
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
        SimpleForm = FormativeTypeRegistry().get('simple').get_form()
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'changed-name'
        }, instance=self.obj)
        f.full_clean()
        self.obj = f.save(commit=False)

    def test_data(self):
        self.assertEqual(self.obj.data['name'], 'changed-name')
