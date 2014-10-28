from django.template import Template, Context
from django.test import TestCase
from formative.models import FormativeBlob


class TestFormativeTags(TestCase):
    def setUp(self):
        f = FormativeBlob.registry.get('simple').form({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        self.obj = f.save()

    def test_get_formative_blob(self):
        t = Template('''{% load formative_tags %}
        {% get_blob 'test-identifier' as simple %}
        {{ simple.unique_identifier }} - {{ simple.data.name }}''')
        self.assertEqual(t.render(Context()).strip(),
                         'test-identifier - test-name')

    def test_get_formative_blob_returns_none(self):
        t = Template('''{% load formative_tags %}
        {% get_blob 'fake-identifier' as simple %}
        {{ simple.unique_identifier }} - {{ simple.data.name }}''')
        self.assertEqual(t.render(Context()).strip(),
                         '-')
