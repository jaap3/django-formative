from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.forms import TypedChoiceField
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from formative.exceptions import FormativeTypeNotRegistered
from formative.registry import FormativeType


@six.add_metaclass(models.SubfieldBase)
class FormativeTypeField(models.Field):
    """
    Allows FormativeType assignment and retrieval.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(FormativeTypeField, self).__init__(*args, **kwargs)

    def get_choices(self):
        """
        Get the formative types for the bound model.
        """
        for item in self.model.registry:
            yield (item.name, item.verbose_name)

    def deconstruct(self):
        """
        Deconstruct the field for migrations
        """
        name, path, args, kwargs = super(
            FormativeTypeField, self).deconstruct()
        del kwargs['max_length']  # remove as it's hardcoded
        return name, path, args, kwargs

    def get_prep_value(self, value):
        """
        Value for database usage
        """
        if isinstance(value, FormativeType):
            return value.name
        return value

    def value_to_string(self, obj):
        """
        Value for serialisation
        """
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        """
        Converts string to FormativeType or None if value is empty
        """
        if not value or isinstance(value, FormativeType):
            return value or None
        try:
            return self.model.registry.get(value)
        except FormativeTypeNotRegistered:
            raise ValidationError(
                _('Invalid type: %(value)s.') % {'value': value})

    def formfield(self, **kwargs):
        """
        TypedChoiceField with all allowed types for the bound model
        """
        defaults = {
            'form_class': TypedChoiceField,
            'choices': self.get_choices(),
            'coerce': self.to_python
        }
        defaults.update(kwargs)
        return super(FormativeTypeField, self).formfield(**defaults)


class HiddenFormativeTypeInput(forms.HiddenInput):
    def render(self, name, value, attrs=None):
        if isinstance(value, FormativeType):
            value = value.name
        return super(
            HiddenFormativeTypeInput, self).render(name, value, attrs=attrs)