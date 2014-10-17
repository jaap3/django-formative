import json
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.db.models.base import ModelBase
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from formative.fields import FormativeTypeField
from formative.registry import FormativeTypeRegistry


class FormativeTypeRegistryMeta(ModelBase):
    """
    BaseFormativeBlob metaclass provides a registry for each subclass.
    """
    def __new__(mcs, name, bases, attrs):
        super_new = super(FormativeTypeRegistryMeta, mcs).__new__
        # Ensure initialization is only performed for subclasses of BaseFormativeBlob
        parents = [b for b in bases if isinstance(b, FormativeTypeRegistryMeta)]
        if not parents:
            return super_new(mcs, name, bases, attrs)

        attrs['registry'] = FormativeTypeRegistry()
        return super_new(mcs, name, bases, attrs)


@python_2_unicode_compatible
class BaseFormativeBlob(six.with_metaclass(FormativeTypeRegistryMeta,
                                           models.Model)):
    """
    Base class for all formative blob types
    """
    formative_type = FormativeTypeField(_('type'))
    json_data = models.TextField(default='{}')

    @classmethod
    def register(cls, *klasses):
        """
        Register a formative type for use with this model
        """
        for klass in klasses:
            cls.registry.register(klass, cls)

    @property
    def data(self):
        """
        Restores the stored json data to the correct python objects.
        """
        data = {}
        json_data = json.loads(self.json_data)
        form = self.formative_type.form(initial=json_data)
        for key, value in json_data.items():
            try:
                data[key] = form.fields[key].clean(value)
            except ValidationError:
                data[key] = None
        return data

    @data.setter
    def data(self, value):
        """
        Store a python data dict as json.
        """
        self.json_data = json.dumps(value, cls=DjangoJSONEncoder)

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.formative_type


@python_2_unicode_compatible
class FormativeBlob(BaseFormativeBlob):
    """
    Simple standalone formative blob
    """
    unique_identifier = models.CharField(
        _('identifier'), max_length=150, unique=True)

    class Meta:
        verbose_name = _('formative blob')
        verbose_name_plural = _('formative blobs')

    def __str__(self):
        return '%s (%s)' % (self.unique_identifier, self.formative_type)


class InlineFormativeBlob(BaseFormativeBlob):
    """
    Formative blob that can be associated with other models
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    sortorder = models.PositiveIntegerField(_('sortorder'), default=0)

    class Meta:
        verbose_name = _('inline formative blob')
        verbose_name_plural = _('inline formative blobs')
        ordering = ('sortorder',)
