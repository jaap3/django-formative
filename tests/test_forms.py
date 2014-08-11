import unittest

from tests.testproject.sample_forms import SimpleForm


class TestSimpleForm(unittest.TestCase):
    def setUp(self):
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        if f.is_valid():
            self.object = f.save()
        else:
            self.fail('SimpleForm is not valid!')

    def test_unique_identifier(self):
        self.assertEqual(self.object.unique_identifier, 'test-identifier')

    def test_unique_identifier_not_in_data(self):
        self.assertFalse('unique_identifier' in self.object.data)

    def test_data(self):
        self.assertEqual(self.object.data['name'], 'test-name')

    def tearDown(self):
        self.object.delete()
