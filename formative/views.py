from __future__ import unicode_literals
from django.contrib.admin.helpers import InlineAdminForm
from django.forms.models import modelform_factory
from django.views.generic import TemplateView
from formative.forms import FormativeTypeForm
from formative.utils import add_field_to_fieldsets


class InlineFormView(TemplateView):
    template_name = 'formative/admin/render_fieldsets.html'
    model = None

    def get_type_from_request(self):
        """
        Get formative type from request
        """
        form_cls = modelform_factory(self.model, form=FormativeTypeForm)
        form = form_cls(self.request.GET)
        if form.is_valid():
            return form.cleaned_data['formative_type']
        return None

    def get_form(self):
        ft = self.get_type_from_request()
        if ft:
            prefix = self.request.GET['prefix']
            initial = {'formative_type': ft.name}
            fieldsets = add_field_to_fieldsets('sortorder', ft.fieldsets)
            return InlineAdminForm(
                None, ft.form(initial=initial, prefix=prefix), fieldsets,
                {}, None)

    def get_context_data(self, **kwargs):
        context = super(InlineFormView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
