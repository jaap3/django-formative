import unittest

from tests.testproject.testapp.forms import SimpleForm


class TestSimpleForm(unittest.TestCase):
    def setUp(self):
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        self.object = f.save()

    def test_unique_identifier(self):
        self.assertEqual(self.object.unique_identifier, 'test-identifier')

    def test_unique_identifier_not_in_data(self):
        self.assertFalse('unique_identifier' in self.object.data)

    def test_data(self):
        self.assertEqual(self.object.data['name'], 'test-name')

    def tearDown(self):
        self.object.delete()


class TestSimpleFormWithInstance(TestSimpleForm):
    def setUp(self):
        super(TestSimpleFormWithInstance, self).setUp()
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'changed-name'
        }, instance=self.object)
        f.full_clean()
        self.object = f.save()

    def test_data(self):
        self.assertEqual(self.object.data['name'], 'changed-name')
