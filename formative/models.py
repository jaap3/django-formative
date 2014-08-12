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
        return json.loads(self.json_data)

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

    def __unicode__(self):
        return '%s (%s)' % (self.unique_identifier, self.formative_type)
