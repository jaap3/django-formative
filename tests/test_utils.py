from unittest import TestCase
from formative.utils import add_field_to_fieldsets


class TestAddFieldToFieldsets(TestCase):
    def test_without_empty_group(self):
        fieldsets = [('test', {'fields': ['example']})]
        updated = add_field_to_fieldsets('added', fieldsets)
        # didn't modify the original
        self.assertEqual(fieldsets, [('test', {'fields': ['example']})])
        self.assertEqual(updated, [
            (None, {'fields': ['added']}),
            ('test', {'fields': ['example']})
        ])

    def test_with_empty_group(self):
        fieldsets = [(None, {'fields': ['example']})]
        updated = add_field_to_fieldsets('added', fieldsets)
        # didn't modify the original
        self.assertEqual(fieldsets, [(None, {'fields': ['example']})])
        self.assertEqual(updated, [
            (None, {'fields': ['added', 'example']})
        ])

    def test_no_need_to_add(self):
        fieldsets = [(None, {'fields': ['example', 'not-added']})]
        updated = add_field_to_fieldsets('not-added', fieldsets)
        self.assertEqual(fieldsets, updated)

    def test_fieldsets_with_tuples(self):
        # Make sure tuples don't mess up the logic
        fieldsets = ((None, {'fields': ('example',)}),)
        updated = add_field_to_fieldsets('added', fieldsets)
        # didn't modify the original
        self.assertEqual(fieldsets, ((None, {'fields': ('example',)}),))
        self.assertEqual(updated, [
            (None, {'fields': ['added', 'example']})
        ])
