from django.core.exceptions import ValidationError
from django.forms import Field, Select
from django.utils.translation import ugettext_lazy as _
from formative import registry
from formative.exceptions import FormativeTypeNotRegistered


class FormativeTypeField(Field):
    widget = Select
    default_error_messages = {
        'invalid': _('Select a valid type. %(value)s is not a known type.')
    }

    def __init__(self, *args, **kwargs):
        super(FormativeTypeField, self).__init__(*args, **kwargs)
        self.widget.choices = self.get_choices()

    def get_choices(self):
        """
        Lazy choices generator as types need time to be
        registered.
        """
        for item in sorted(registry.items()):
            yield item

    def to_python(self, value):
        """
        Validates that the input is a registered type.
        Returns a FormativeType instance or None for emtpy values
        """
        if value in self.empty_values:
            return None
        try:
            value = registry[value]
        except FormativeTypeNotRegistered:
            raise ValidationError(self.error_messages['invalid'] % {
                'value': value
            }, code='invalid')
        return value
