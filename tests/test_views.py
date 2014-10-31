from django.test import RequestFactory, TestCase
from formative.models import InlineFormativeBlob
from formative.views import InlineFormView
from tests.testproject.testapp.forms import SimpleForm


class TestInlineFormView(TestCase):
    def setUp(self):
        view = InlineFormView.as_view(model=InlineFormativeBlob)
        request = RequestFactory().get(
            '/', {'formative_type': 'simple', 'prefix': 'test-prefix'})
        self.response = view(request)

    def test_template(self):
        self.assertTemplateUsed(
            self.response, 'formative/admin/render_fieldsets.html')

    def test_correct_form_in_context(self):
        self.assertIsInstance(
            self.response.context_data['form'].form, SimpleForm)

    def test_form_has_correct_prefix(self):
        self.assertEqual(
            'test-prefix', self.response.context_data['form'].form.prefix)

    def test_output(self):
        self.assertContains(
            self.response, '<input id="id_test-prefix-formative_type"'
                           ' name="test-prefix-formative_type"'
                           ' type="hidden" value="simple" />')


class TestInlineFormViewInvalidRequests(TestCase):
    def setUp(self):
        self.view = InlineFormView.as_view(model=InlineFormativeBlob)

    def test_missing_get_parameters(self):
        request = RequestFactory().get('/')
        response = self.view(request)
        self.assertContains(
            response, '<p class="errornote">'
                      'Invalid formative type or missing parameters</p>')

    def test_bad_formative_type(self):
        request = RequestFactory().get(
            '/', {'formative_type': 'invalid', 'prefix': 'test-prefix'})
        response = self.view(request)
        self.assertContains(
            response, '<li>This field is required.</li>')

    def test_no_prefix(self):
        request = RequestFactory().get('/', {'formative_type': 'simple'})
        response = self.view(request)
        self.assertContains(
            response, '<p class="errornote">'
                      'Invalid formative type or missing parameters</p>')
