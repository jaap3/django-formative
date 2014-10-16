import json
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import ugettext_lazy as _
from formative import registry
from formative.exceptions import FormativeTypeNotRegistered
from formative.fields import FormativeTypeField
from formative.registry import FormativeType


class FormativeTypeModelField(models.Field):
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['null'] = True
        super(FormativeTypeModelField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(
            FormativeTypeModelField, self).deconstruct()
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

    def from_db_value(self, value, connection):
        if value is None:
            return value
        return registry[value]

    def to_python(self, value):
        if value is None or isinstance(value, FormativeType):
            return value
        try:
            return registry[value]
        except FormativeTypeNotRegistered:
            raise ValidationError(
                _('Invalid type: %(value)s.') % {'value': value})

    def formfield(self, **kwargs):
        defaults = {'form_class': FormativeTypeField}
        defaults.update(kwargs)
        return super(FormativeTypeModelField, self).formfield(**defaults)


class BaseFormativeBlob(models.Model):
    formative_type = FormativeTypeModelField(_('type'))
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
        form = self.formative_type.form(initial=json_data)
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
    unique_identifier = models.CharField(
        _('identifier'), max_length=150, unique=True)

    class Meta:
        verbose_name = _('formative blob')
        verbose_name_plural = _('formative blobs')
        ordering = ('formative_type', 'unique_identifier')

    def __str__(self):
        return '%s (%s)' % (self.unique_identifier, self.formative_type)


class InlineFormativeBlob(BaseFormativeBlob):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    sortorder = models.PositiveIntegerField(_('sortorder'), default=0)

    class Meta:
        verbose_name = _('inline formative blob')
        verbose_name_plural = _('inline formative blobs')
        ordering = ('sortorder',)
