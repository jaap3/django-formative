import json
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _
from formative import registry


def formative_type_validator(value):
    if value not in registry:
        raise ValidationError(_(
            'Invalid formative type \'%(type)s\' is not one of the'
            ' available types.') % {'type': value})


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
        try:
            json_data = json.loads(self.json_data)
        except ValueError:
            json_data = {}
        form = (registry.get(self.formative_type).form(initial=json_data))
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


class InlineFormativeBlob(BaseFormativeBlob):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    sortorder = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _('inline formative blob')
        verbose_name_plural = _('inline formative blobs')
        ordering = ('sortorder',)
