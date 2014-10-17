from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.contenttypes.admin import GenericStackedInline
from django.forms.models import modelform_factory
from django.template.response import TemplateResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from formative.forms import FormativeTypeForm
from formative.formsets import (
    FormativeFormset, InlineFormativeBlobAdminFormSet)
from formative.models import FormativeBlob, InlineFormativeBlob


class FormativeBlobAdmin(admin.ModelAdmin):
    search_fields = ('unique_identifier',)
    list_filter = ('formative_type',)
    list_display = ('unique_identifier', 'formative_type')
    ordering = ('formative_type', 'unique_identifier')

    def get_type_from_request(self, request):
        """
        Get formative type from request
        """
        form_cls = modelform_factory(self.model, form=FormativeTypeForm)
        form = form_cls(request.GET)
        if form.is_valid():
            return form.cleaned_data['formative_type']
        return None

    def get_form(self, request, obj=None, **kwargs):
        """
        Get a form for the add/change view.
        """
        ft = (obj.formative_type if obj
              else self.get_type_from_request(request))
        kwargs['form'] = ft.form
        return super(FormativeBlobAdmin, self).get_form(
            request, obj=obj, **kwargs)

    def get_fieldsets(self, request, obj=None):
        """
        Get fieldset definitions for the add/change view.
        """
        ft = (obj.formative_type if obj
              else self.get_type_from_request(request))
        fieldsets = ft.fieldsets
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
        return fieldsets or super(
            FormativeBlobAdmin, self).get_fieldsets(request, obj)

    def add_view(self, request, **kwargs):
        """
        Checks if a content type is selected, if so delegates to super.
        If not, self.select_content_type_view is called.
        """
        ft = self.get_type_from_request(request)
        if ft:
            return super(FormativeBlobAdmin, self).add_view(request, **kwargs)
        else:
            return self.select_type_view(request)

    def select_type_view(self, request):
        """
        Used in the add view to render the "select a formative type" form
        and handle its errors.
        """
        form_cls = modelform_factory(self.model, form=FormativeTypeForm)
        if '_next' in request.GET:
            form = form_cls(request.GET)
        else:
            form = form_cls()
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


class BaseFormativeInline(GenericStackedInline):
    formset = FormativeFormset
    extra = 0


class FormativeBlobInline(BaseFormativeInline):
    model = InlineFormativeBlob


class InlineFormativeBlobAdmin(admin.ModelAdmin):
    def get_inline_formsets(self, request, formsets,
                            inline_instances, obj=None):
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            if isinstance(inline, BaseFormativeInline):
                inline_admin_formset = InlineFormativeBlobAdminFormSet(
                    inline, formset, [], {}, {}, model_admin=self)
            else:
                fieldsets = list(
                    inline.get_fieldsets(request, obj))
                readonly = list(
                    inline.get_readonly_fields(request, obj))
                prepopulated = dict(
                    inline.get_prepopulated_fields(request, obj))
                inline_admin_formset = helpers.InlineAdminFormSet(
                    inline, formset, fieldsets, prepopulated,
                    readonly, model_admin=self)
            inline_admin_formsets.append(inline_admin_formset)
        return inline_admin_formsets


admin.site.register(FormativeBlob, FormativeBlobAdmin)
