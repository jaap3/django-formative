from copy import deepcopy
from django.contrib.admin import AdminSite
from django.test import TestCase, RequestFactory
from formative.formsets import InlineFormativeBlobAdminFormSet
from formative.models import InlineFormativeBlob
from tests.testproject.testapp.admin import BookAdmin
from tests.testproject.testapp.models import Book


class MockUser(object):
    def has_perm(self, *args, **kwargs):
        return True


class TestAdd(TestCase):
    def setUp(self):
        self.admin = BookAdmin(Book, AdminSite())
        self.request = RequestFactory().get('/add/')


class TestChange(TestCase):
    def setUp(self):
        self.admin = BookAdmin(Book, AdminSite())
        self.book = Book(title='Gun Machine')
        self.book.save()
        InlineFormativeBlob(
            content_object=self.book, formative_type='simple', sortorder=0
        ).save()
        InlineFormativeBlob(
            content_object=self.book, formative_type='fancy', sortorder=0
        ).save()
        self.request = RequestFactory().get('/edit/')
        self.request.user = MockUser()
        response = self.admin.change_view(self.request, str(self.book.pk))
        self.formsets = response.context_data['inline_admin_formsets']
        self.forms = [form for form in self.formsets[0]]

    def test_formsets(self):
        self.assertIsInstance(
            self.formsets[0], InlineFormativeBlobAdminFormSet)

    def test_forms(self):
        self.assertEqual(len(self.forms), 3)

    def test_form_1_form(self):
        self.assertIsInstance(
            self.forms[0].form,
            InlineFormativeBlob.registry.get('simple').form)

    def test_form_2_form(self):
        self.assertIsInstance(
            self.forms[1].form,
            InlineFormativeBlob.registry.get('fancy').form)

    def test_form_1_type(self):
        self.assertEqual(
            self.forms[0].form.formative_type,
            InlineFormativeBlob.registry.get('simple'))

    def test_form_2_type(self):
        self.assertEqual(
            self.forms[1].form.formative_type,
            InlineFormativeBlob.registry.get('fancy'))

    def test_form_1_fieldsets(self):
        expected = deepcopy(
            InlineFormativeBlob.registry.get('simple').fieldsets)
        expected[0][1]['fields'] = ['sortorder'] + expected[0][1]['fields']
        self.assertEqual(
            self.forms[0].fieldsets, expected)

    def test_form_2_fieldsets(self):
        expected = deepcopy(
            InlineFormativeBlob.registry.get('fancy').fieldsets)
        expected[0][1]['fields'] = ['sortorder'] + expected[0][1]['fields']
        self.assertEqual(
            self.forms[1].fieldsets, expected)
