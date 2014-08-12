from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from formative.models import FormativeBlob
from formative.registry import FormativeTypeRegistry


class FormativeTypeForm(forms.Form):
    formative_type = forms.ChoiceField(_('formative type'))

    def __init__(self, *args, **kwargs):
        super(FormativeTypeForm, self).__init__(*args, **kwargs)
        # Set the choices here so they have had time to register.
        self.fields['formative_type'].choices = FormativeTypeRegistry().items()


class FormativeBlobAdmin(admin.ModelAdmin):
    def add_view(self, request, form_url='', extra_context=None):
        """
        Checks if a content type is selected, if so delegates to super.
        If not, self.select_content_type_view is called.
        """
        form = FormativeTypeForm(request.GET)
        if form.is_valid():
            return super(FormativeBlobAdmin,
                         self).add_view(request, form_url=form_url,
                                        extra_context=extra_context)
        else:
            return self.select_formative_type_view(request)

    def select_formative_type_view(self, request):
        """
        Used in the add view to render the "select a formative type" form
        and handle its errors.
        """
        if '_next' in request.GET:
            form = FormativeTypeForm(request.GET)
        else:
            form = FormativeTypeForm()
        opts = self.model._meta
        adminform = helpers.AdminForm(
            form, [(None, {'fields': ['formative_type']})], {}, ())
        context = {
            'title': _('Add %s') % force_text(opts.verbose_name),
            'adminform': adminform,
            'is_popup': IS_POPUP_VAR in request.REQUEST,
            'media': self.media + adminform.media,
            'errors': helpers.AdminErrorList(form, []),
            'app_label': opts.app_label,
            'opts': opts
        }
        return TemplateResponse(
            request, 'formative/admin/formative_type_form.html',
            context, current_app=self.admin_site.name)


admin.site.register(FormativeBlob, FormativeBlobAdmin)
