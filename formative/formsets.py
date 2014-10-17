from django.contrib.admin.helpers import InlineAdminForm, InlineAdminFormSet
from django.contrib.contenttypes.generic import BaseGenericInlineFormSet
from django.forms.models import modelform_factory
from django.utils import six
from formative.forms import FormativeTypeForm


class FormativeFormsetMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name != 'FormativeFormset' and 'form' in attrs:
            # Get model from form
            model = attrs['form']._meta.model
            # Then swap it for our FormativeMetaForm
            attrs['form'] = FormativeMetaForm(model)
        return super(
            FormativeFormsetMeta, mcs).__new__(mcs, name, bases, attrs)


class FormativeMetaForm(object):
    base_fields = ['formative_type']
    ct_field = 'content_type'
    ct_fk_field = 'object_id'

    def __init__(self, model):
        self.model = model

    def __call__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        form = modelform_factory(self.model, FormativeTypeForm)
        if instance:
            form = instance.formative_type.get_form(
                exclude=[self.ct_field, self.ct_fk_field])
        return form(*args, **kwargs)


@six.add_metaclass(FormativeFormsetMeta)
class FormativeFormset(BaseGenericInlineFormSet):
    pass


class InlineFormativeBlobAdminFormSet(InlineAdminFormSet):
    def get_fieldsets(self, form):
        fieldsets = None
        if hasattr(form, 'formative_type'):
            fieldsets = form.formative_type.fieldsets
        if fieldsets is None:
            fields = []
            for field in form.base_fields:
                fields.append(field)
            fieldsets = [(None, {'fields': fields})]
        else:
            # user defined fieldsets, make sure sortorder
            # is in there!
            found = False
            for fieldset in fieldsets:
                if 'sortorder' in fieldset[1].get('fields', []):
                    found = True
                    break
            if not found:
                fieldsets = ([(None, {'fields': ['sortorder']})]
                             + list(fieldsets))
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