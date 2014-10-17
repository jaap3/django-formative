from django.db import models
from django.core.exceptions import ValidationError
from django.forms import TypedChoiceField
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from formative.exceptions import FormativeTypeNotRegistered
from formative.registry import FormativeType


@six.add_metaclass(models.SubfieldBase)
class FormativeTypeField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['null'] = True
        super(FormativeTypeField, self).__init__(*args, **kwargs)

    def get_choices(self):
        for item in self.model().registry:
            yield (item.name, item.verbose_name)

    def deconstruct(self):
        name, path, args, kwargs = super(
            FormativeTypeField, self).deconstruct()
        del kwargs['max_length']
        del kwargs['null']
        return name, path, args, kwargs

    def get_prep_value(self, value):
        if isinstance(value, FormativeType):
            return value.name
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if not value or isinstance(value, FormativeType):
            return value or None
        try:
            return self.model().registry.get(value)
        except FormativeTypeNotRegistered:
            raise ValidationError(
                _('Invalid type: %(value)s.') % {'value': value})

    def formfield(self, **kwargs):
        defaults = {
            'form_class': TypedChoiceField,
            'choices': self.get_choices(),
            'coerce': self.to_python
        }
        defaults.update(kwargs)
        return super(FormativeTypeField, self).formfield(**defaults)
