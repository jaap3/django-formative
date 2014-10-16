from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from formative.forms import FormativeTypeForm
from formative.models import FormativeBlob
from formative.utils import get_type_from_request


class FormativeBlobAdmin(admin.ModelAdmin):
    search_fields = ('unique_identifier',)
    list_filter = ('formative_type',)
    list_display = ('unique_identifier', 'formative_type')
    ordering = ('unique_identifier', 'formative_type')

    def get_form(self, request, obj=None, **kwargs):
        """
        Get a form for the add/change view.
        """
        ft = (obj.formative_type if obj else get_type_from_request(request))
        if ft:
            kwargs['form'] = ft.get_form(request, obj, **kwargs)
        return super(
            FormativeBlobAdmin, self).get_form(request, obj=obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        """
        Get fieldset definition for the add/change view.
        """
        ft = (obj.formative_type if obj else get_type_from_request(request))
        fieldsets = None
        if ft:
            fieldsets = ft.get_fieldsets(request, obj)
            if fieldsets:
                # user defined fieldsets, make sure unique_identifier
                # is in there!
                found = False
                for fieldset in fieldsets:
                    if 'unique_identifier' in fieldset[1].get('fields', []):
                        found = True
                        break
                if not found:
                    fieldsets = ([(None, {'fields': ['unique_identifier']})]
                                 + list(fieldsets))
        if fieldsets is None:
            fieldsets = super(
                FormativeBlobAdmin, self).get_fieldsets(request, obj)
        return fieldsets

    def add_view(self, request, **kwargs):
        """
        Checks if a content type is selected, if so delegates to super.
        If not, self.select_content_type_view is called.
        """
        ft = get_type_from_request(request)
        if ft:
            return super(FormativeBlobAdmin, self).add_view(request, **kwargs)
        else:
            return self.select_type_view(request)

    def select_type_view(self, request):
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
