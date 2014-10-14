from django import forms
from django.contrib import admin
from django.contrib.admin import helpers
from django.contrib.admin.helpers import InlineAdminFormSet, InlineAdminForm
from django.contrib.contenttypes.admin import GenericStackedInline
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet
from django.utils.translation import ugettext_lazy as _
from formative import registry
from formative.models import InlineFormativeBlob
from tests.testproject.testapp.models import Book


class FormativeTypeForm(forms.ModelForm):
    formative_type = forms.ChoiceField(_('formative type'))

    class Meta:
        model = InlineFormativeBlob
        fields = ['formative_type']

    def __init__(self, *args, **kwargs):
        super(FormativeTypeForm, self).__init__(*args, **kwargs)
        # Set the choices here so they have had time to register.
        self.fields['formative_type'].choices = sorted(registry.items())


class FormativeFormsetMeta(type):
    def __new__(cls, name, parents, attrs):
        if name != 'FormativeFormset' and 'form' in attrs:
            # Thwart all attempts to swap out FormativeMetaForm
            del attrs['form']
        return super(
            FormativeFormsetMeta, cls).__new__(cls, name, parents, attrs)


class FormativeMetaForm(object):
    base_fields = FormativeTypeForm.base_fields

    @staticmethod
    def get_type_from_object(obj):
        """
        Get formative type from object
        """
        ft = obj.formative_type
        if ft:
            return registry.get(ft)
        return None

    def __call__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        form = FormativeTypeForm
        if instance:
            ft = self.get_type_from_object(instance)
            if ft:
                form = ft.form
        return form(*args, **kwargs)


class FormativeFormset(BaseGenericInlineFormSet):
    __metaclass__ = FormativeFormsetMeta
    form = FormativeMetaForm()


class InlineFormativeBlobAdmin(GenericStackedInline):
    formset = FormativeFormset
    model = InlineFormativeBlob
    extra = 0


class InlineFormativeBlobAdminFormSet(InlineAdminFormSet):
    def get_fieldsets(self, form, obj=None):
        fieldsets = None
        if hasattr(form, 'formative_type'):
            ft = registry.get(form.formative_type)
            if ft:
                fieldsets = ft.get_fieldsets(None, obj)
        return fieldsets or [(None, {'fields': form.fields})]

    def __iter__(self):
        for form, original in zip(
                self.formset.initial_forms, self.formset.get_queryset()):
            view_on_site_url = self.opts.get_view_on_site_url(original)
            yield InlineAdminForm(
                self.formset, form, self.get_fieldsets(form, original),
                self.prepopulated_fields, original, self.readonly_fields,
                model_admin=self.opts, view_on_site_url=view_on_site_url)
        for form in self.formset.extra_forms:
            yield InlineAdminForm(
                self.formset, form, self.get_fieldsets(form),
                self.prepopulated_fields, None, self.readonly_fields,
                model_admin=self.opts)
        yield InlineAdminForm(
            self.formset, self.formset.empty_form,
            self.get_fieldsets(self.formset.empty_form),
            self.prepopulated_fields, None, self.readonly_fields,
            model_admin=self.opts)


class BookAdmin(admin.ModelAdmin):
    inlines = [InlineFormativeBlobAdmin]

    def get_inline_formsets(
            self, request, formsets, inline_instances, obj=None):
        inline_admin_formsets = []
        for inline, formset in zip(inline_instances, formsets):
            if isinstance(inline, InlineFormativeBlobAdmin):
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


admin.site.register(Book, BookAdmin)
