from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.options import IS_POPUP_VAR
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from formative.models import FormativeBlob
from formative import registry


class FormativeTypeForm(forms.Form):
    formative_type = forms.ChoiceField(_('formative type'))

    def __init__(self, *args, **kwargs):
        super(FormativeTypeForm, self).__init__(*args, **kwargs)
        # Set the choices here so they have had time to register.
        self.fields['formative_type'].choices = sorted(
            registry.items())


class FormativeBlobAdmin(admin.ModelAdmin):
    search_fields = ('unique_identifier',)
    list_filter = ('formative_type',)
    list_display = ('unique_identifier', 'get_formative_type_display')
    ordering = ('unique_identifier', 'formative_type')

    def get_formative_type_display(self, obj):
        ft = self.get_formative_type(obj=obj)
        if ft:
            return ft.verbose_name
    get_formative_type_display.short_description = _('type')

    def get_formative_type(self, request=None, obj=None):
        """
        Get the formative type definition for an object OR based on
        the request.
        """
        ft = None
        if request and obj is None:
            # No object, try to get the content type from the request params
            form = FormativeTypeForm(request.GET)
            if form.is_valid():
                ft = form.cleaned_data['formative_type']
        elif obj:
            ft = obj.formative_type
        if ft:
            return registry.get(ft)
        return None

    def get_form(self, request, obj=None, **kwargs):
        """
        Get a form for the add/change view.
        """
        formative_type = self.get_formative_type(request, obj)
        if formative_type:
            kwargs['form'] = formative_type.get_form(request, obj, **kwargs)
        return super(FormativeBlobAdmin,
                     self).get_form(request, obj=obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        """
        Get fieldset definition for the add/change view.
        """
        formative_type = self.get_formative_type(request, obj)
        fieldsets = None
        if formative_type:
            fieldsets = formative_type.get_fieldsets(request, obj)
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
            fieldsets = super(FormativeBlobAdmin,
                              self).get_fieldsets(request, obj)
        return fieldsets

    def add_view(self, request, form_url='', extra_context=None):
        """
        Checks if a content type is selected, if so delegates to super.
        If not, self.select_content_type_view is called.
        """
        formative_type = self.get_formative_type(request)
        if formative_type:
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
