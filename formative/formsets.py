import sys
from django.contrib.admin.helpers import InlineAdminForm, InlineAdminFormSet
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet
from django.forms.models import modelform_factory
from django.utils import six
from formative.forms import FormativeTypeForm
from formative.utils import add_field_to_fieldsets


class FormativeFormsetMeta(type):
    """
    This metaclass prevents Django from overriding our MetaForm and allows
    us to initialize the metaform with the correct model class.
    """
    def __new__(mcs, name, bases, attrs):
        if name != 'FormativeFormset' and 'form' in attrs:
            # Get model from form
            model = attrs['form']._meta.model
            # Then swap it for our FormativeMetaForm
            attrs['form'] = FormativeMetaForm(model)
        return super(
            FormativeFormsetMeta, mcs).__new__(mcs, name, bases, attrs)


class FormativeMetaForm(object):
    """
    This object tricks django's formsets into using the forms we want.
    """
    base_fields = ['formative_type']

    def __init__(self, model):
        self.model = model

    def __call__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        form_class = modelform_factory(self.model, FormativeTypeForm)
        if instance:
            form_class = instance.formative_type.form
        elif 'data' in kwargs:
            form = form_class(**kwargs)
            if form.is_valid():
                form_class = form.cleaned_data['formative_type'].form
        return form_class(**kwargs)


@six.add_metaclass(FormativeFormsetMeta)
class FormativeFormset(BaseGenericInlineFormSet):
    """
    A generic inline formset subclass that uses the FormativeMetaForm to
    hand out the correct form based on model/request data.
    """


class BaseInlineFormativeAdminFormSet(InlineAdminFormSet):
    def get_fieldsets(self, form):
        fieldsets = [(None, {'fields': form.base_fields})]
        if hasattr(form, 'formative_type'):
            ft = form.formative_type
            fieldsets = add_field_to_fieldsets('sortorder', ft.fieldsets)
        return fieldsets

    def __iter__(self):
        for form, original in zip(
                self.formset.initial_forms, self.formset.get_queryset()):
            view_on_site_url = self.opts.get_view_on_site_url(original)
            yield InlineAdminForm(
                self.formset, form, self.get_fieldsets(form),
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


class SortedInlineFormativeAdminFormSet(BaseInlineFormativeAdminFormSet):
    def sort_key(self, admin_form):
        try:
            return int(admin_form.form['sortorder'].value())
        except (KeyError, TypeError, ValueError):
            return sys.maxint
        return -1

    def __iter__(self):
        forms = list(
            super(SortedInlineFormativeAdminFormSet, self).__iter__())
        for form in sorted(forms[:-1], key=self.sort_key):
            yield form
        yield forms[-1]  # The empty form
