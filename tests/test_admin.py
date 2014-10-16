from django.contrib.admin import AdminSite
from django.test import RequestFactory, TestCase
from formative import registry
from formative.admin import FormativeTypeForm, FormativeBlobAdmin
from formative.models import FormativeBlob
from tests.testproject.testapp.forms import SimpleForm


class MockUser(object):
    def has_perm(self, *args, **kwargs):
        return True


class TestFormativeTypeFormValidation(TestCase):
    def test_invalid_type(self):
        f = FormativeTypeForm({'formative_type': 'invalid'})
        self.assertFalse(f.is_valid())
        self.assertEqual(f.errors, {
            'formative_type': [
                'Select a valid type. invalid is not a known type.']
        })

    def test_valid_type(self):
        f = FormativeTypeForm({'formative_type': 'simple'})
        self.assertTrue(f.is_valid())


class TestSelectType(TestCase):
    def setUp(self):
        self.admin = FormativeBlobAdmin(FormativeBlob, AdminSite())
        self.request = RequestFactory().get('/add/')

    def test_add_view_delegates_to_select_formative_type_view(self):
        response = self.admin.add_view(self.request)
        self.assertEqual(
            response.template_name, 'formative/admin/formative_type_form.html')

    def test_add_returns_formative_type_form(self):
        response = self.admin.add_view(self.request)
        self.assertIsInstance(response.context_data['adminform'].form,
                              FormativeTypeForm)

    def test_add_with_next_param_validates_requested_type(self):
        response = self.admin.add_view(RequestFactory().get('/add/', {
            'formative_type': 'invalid', '_next': None
        }))
        self.assertEqual(response.context_data['adminform'].form.errors, {
            'formative_type': [
                'Select a valid type. invalid is not a known type.']
        })

    def test_add_without_next_param_and_invalid_type(self):
        response = self.admin.add_view(RequestFactory().get('/add/', {
            'formative_type': 'invalid',
        }))
        self.assertEqual(
            response.template_name, 'formative/admin/formative_type_form.html')
        self.assertEqual(response.context_data['adminform'].form.errors, {})

    def test_add_with_valid_type_renders_add(self):
        request = RequestFactory().get('/add/', {
            'formative_type': 'simple',
        })
        request.user = MockUser()
        response = self.admin.add_view(request)
        self.assertIn('admin/change_form.html', response.template_name)


class TestAddAndChange(TestCase):
    def setUp(self):
        self.admin = FormativeBlobAdmin(FormativeBlob, AdminSite())
        self.request = RequestFactory().get('/add/', {
            'formative_type': 'simple',
        })
        self.request.user = MockUser()
        self.SimpleForm = registry.get('simple').form

    def test_add_gets_correct_form(self):
        response = self.admin.add_view(self.request)
        self.assertIsInstance(
            response.context_data['adminform'].form, self.SimpleForm)

    def test_change_gets_correct_form(self):
        f = self.SimpleForm({
            'unique_identifier': 'test-identifier',
            'name': 'test-name'
        })
        f.full_clean()
        obj = f.save()
        response = self.admin.change_view(self.request, str(obj.pk))
        self.assertIsInstance(response.context_data['adminform'].form,
                              SimpleForm)
        obj.delete()


class TestGetFieldsets(TestCase):
    def setUp(self):
        self.admin = FormativeBlobAdmin(FormativeBlob, AdminSite())

    def test_get_undefined_fieldsets(self):
        request = RequestFactory().get('/add/', {
            'formative_type': 'simple',
        })
        self.assertEqual(self.admin.get_fieldsets(request), [
            (None, {'fields': ['unique_identifier', 'name']})
        ])

    def test_get_defined_fieldsets(self):
        request = RequestFactory().get('/add/', {
            'formative_type': 'fieldset-identifier',
        })
        self.assertEqual(self.admin.get_fieldsets(request),  [
            (None, {'fields': ['unique_identifier']}),
            ('Title', {'fields': ['title']}),
            ('Body', {'fields': ['body']})
        ])

    def test_get_fieldsets_adds_unique_identifier(self):
        request = RequestFactory().get('/add/', {
            'formative_type': 'fieldset-no-identifier',
        })
        self.assertEqual(self.admin.get_fieldsets(request),  [
            (None, {'fields': ['unique_identifier']}),
            ('Title', {'fields': ['title']}),
            ('Body', {'fields': ['body']})
        ])
