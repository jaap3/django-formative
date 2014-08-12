import unittest
from django.core.exceptions import ValidationError
from formative.models import FormativeBlob


class TestFormativeTypeValidation(unittest.TestCase):
    def test_invalid_type(self):
        blob = FormativeBlob(unique_identifier='invalid',
                             formative_type='invalid',
                             json_data='{}')
        self.assertRaisesRegexp(ValidationError, 'Invalid formative type',
                                blob.full_clean)

    def test_valid_type(self):
        blob = FormativeBlob(unique_identifier='valid',
                             formative_type='simple',
                             json_data='{}')
        try:
            blob.full_clean()
        except ValidationError as e:
            self.fail('ValidationError raised: %s' % e)


class TestFormativeBlob(unittest.TestCase):
    def setUp(self):
        self.blob = FormativeBlob(unique_identifier='identifier',
                                  formative_type='simple',
                                  json_data='{}')
        self.blob.save()

    def test_unicode(self):
        self.assertEqual(unicode(self.blob), 'identifier (simple)')
