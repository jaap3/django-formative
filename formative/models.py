import json
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _
from formative.registry import FormativeTypeRegistry


def formative_type_validator(value):
    if value not in FormativeTypeRegistry():
        raise ValidationError(_('Invalid formative type %r '
                                'is not one of the available types.') % value)


class BaseFormativeBlob(models.Model):
    formative_type = models.CharField(max_length=150,
                                      validators=[formative_type_validator])
    json_data = models.TextField()

    @property
    def data(self):
        """
        Restores the stored json data to the correct python objects.
        """
        data = {}
        json_data = json.loads(self.json_data)
        form = (FormativeTypeRegistry().get(self.formative_type)
                .form(initial=json_data))
        for key, value in json_data.items():
            try:
                data[key] = form.fields[key].to_python(value)
            except ValidationError:
                data[key] = None
        return data

    @data.setter
    def data(self, value):
        self.json_data = json.dumps(value, cls=DjangoJSONEncoder)

    class Meta:
        abstract = True


class FormativeBlob(BaseFormativeBlob):
    unique_identifier = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = _('formative blob')
        verbose_name_plural = _('formative blobs')

    def __str__(self):
        return '%s (%s)' % (self.unique_identifier, self.formative_type)
