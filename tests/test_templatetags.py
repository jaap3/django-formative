from django.template import Template, Context
from django.test import TestCase
from formative import registry


class TestFormativeTags(TestCase):
    def setUp(self):
        f = registry.get('simple').form({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        self.obj = f.save()

    def test_get_formative_blob(self):
        t = Template('''{% load formative_tags %}
        {% get_formative_blob 'test-identifier' as simple %}
        {{ simple.unique_identifier }} - {{ simple.data.name }}''')
        self.assertEqual(t.render(Context()).strip(),
                         'test-identifier - test-name')
