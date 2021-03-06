from __future__ import unicode_literals
from django.contrib.admin.helpers import InlineAdminForm
from django.views.generic import TemplateView
from formative.utils import add_field_to_fieldsets


class InlineFormView(TemplateView):
    template_name = 'formative/admin/render_fieldsets.html'
    model = None

    def get_type_from_request(self):
        """
        Get formative type from request
        """
        form = self.model.registry.type_select_form(self.request.GET)
        if form.is_valid():
            return form.cleaned_data['formative_type']
        return None

    def get_form(self):
        ft = self.get_type_from_request()
        prefix = self.request.GET.get('prefix')
        form = fieldsets = None
        if ft and prefix:
            initial = {'formative_type': ft.name}
            fieldsets = add_field_to_fieldsets('sortorder', ft.fieldsets)
            form = ft.form(initial=initial, prefix=prefix)
        elif prefix:
            form = self.model.registry.type_select_form(
                self.request.GET, prefix=prefix)
            fieldsets = [(None, {'fields': form.base_fields})]
        if form and fieldsets:
            return InlineAdminForm(None, form, fieldsets, {}, None)
        return None

    def get_context_data(self, **kwargs):
        context = super(InlineFormView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
