import datetime
from decimal import Decimal
from django.test import TestCase
from formative.models import FormativeBlob
from tests.testproject.testapp.models import Book


class TestSimpleForm(TestCase):
    def setUp(self):
        SimpleForm = FormativeBlob.registry.get('simple').form
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        self.obj = f.save()

    def test_unique_identifier(self):
        self.assertEqual(self.obj.unique_identifier, 'test-identifier')

    def test_unique_identifier_not_in_data(self):
        self.assertFalse('unique_identifier' in self.obj.data)

    def test_data(self):
        self.assertEqual(self.obj.data['name'], 'test-name')


class TestSimpleFormWithInstance(TestSimpleForm):
    def setUp(self):
        super(TestSimpleFormWithInstance, self).setUp()
        SimpleForm = FormativeBlob.registry.get('simple').form
        self.f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'changed-name'
        }, instance=self.obj)
        self.f.full_clean()
        self.obj = self.f.save()

    def test_field_value(self):
        self.assertEqual(self.f['name'].value(), 'changed-name')

    def test_data(self):
        self.assertEqual(self.obj.data['name'], 'changed-name')


class TestSimpleFormWithInstanceAndInitial(TestCase):
    def setUp(self):
        SimpleForm = FormativeBlob.registry.get('simple').form
        f = SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        obj = f.save()
        self.f = SimpleForm(initial={
            'unique_identifier': 'test-identifier',
            'name': 'changed-name'
        }, instance=obj)

    def test_field_value(self):
        self.assertEqual(self.f['name'].value(), 'changed-name')


class TestFancyForm(TestCase):
    def setUp(self):
        self.FancyForm = FormativeBlob.registry.get('fancy').form

    def test_serializes_fancy_form(self):
        f = self.FancyForm({
            'unique_identifier': 'fancy',
            'is_fancy': 'true', 'favorite_color': 'blue',
            'date_of_birth': '1967-05-13', 'income': '1967.05',
            'number_of_fingers': '10', 'family_members': ['mom', 'dad'],
            'time_of_day': '16:20'
        })
        f.full_clean()
        obj = f.save()
        self.assertEqual(obj.data, {
            'is_fancy': True,
            'favorite_color': 'blue',
            'date_of_birth': datetime.date(1967, 5, 13),
            'income': Decimal('1967.05'),
            'number_of_fingers': 10,
            'family_members': ['mom', 'dad'],
            'time_of_day': datetime.time(16, 20)
        })


class TestRelatedForm(TestCase):
    def setUp(self):
        self.RelatedForm = FormativeBlob.registry.get('related').form
        self.book = Book(title='Gunmachine')
        self.book.save()

    def test_serializes_relation(self):
        f = self.RelatedForm({
            'unique_identifier': 'related',
            'book': self.book.pk
        })
        f.full_clean()
        obj = f.save()
        self.assertEqual(obj.data, {
            'book': self.book
        })

    def test_data_does_not_break_on_deletion(self):
        f = self.RelatedForm({
            'unique_identifier': 'related',
            'book': self.book.pk
        })
        f.full_clean()
        obj = f.save()
        self.book.delete()
        self.assertEqual(obj.data, {
            'book': None
        })
