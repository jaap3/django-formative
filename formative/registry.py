from collections import Container, Iterable, Sized
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six
from django.utils.functional import cached_property
from django.utils.text import camel_case_to_spaces
from formative.exceptions import FormativeTypeNotRegistered
from formative.utils import formative_form_factory


class FormativeTypeBase(type):
    def __new__(cls, name, parents, attrs):
        if 'name' not in attrs:
            attrs['name'] = camel_case_to_spaces(name).lower()
        if 'verbose_name' not in attrs:
            attrs['verbose_name'] = attrs['name'].title()
        if 'fieldsets' not in attrs:
            attrs['fieldsets'] = None
        return super(FormativeTypeBase, cls).__new__(cls, name, parents, attrs)


@python_2_unicode_compatible
@six.add_metaclass(FormativeTypeBase)
class FormativeType(object):
    def __init__(self, model):
        self.model = model

    @cached_property
    def form(self):
        form = formative_form_factory(self.model, self.form_class)
        form.formative_type = self
        return form

    def __str__(self):
        return self.verbose_name


class FormativeTypeRegistry(Sized, Iterable, Container):
    def __init__(self):
        self.__registry = {}

    def __contains__(self, name):
        return name in self.__registry

    def __iter__(self):
        for key, value in sorted(self.__registry.items()):
            yield value

    def __len__(self):
        return len(self.__registry)

    def register(self, name, cls, model):
        self.__registry[name] = cls(model)

    def get(self, name):
        try:
            return self.__registry[name]
        except KeyError:
            raise FormativeTypeNotRegistered


def autodiscover():
    """
    Auto-discover INSTALLED_APPS formative_types.py modules and fail silently
    if not present.
    """
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's formative_types module.
        try:
            import_module('%s.formative_types' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an formative_types module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'formative_types'):
                raise  # pragma: nocover
