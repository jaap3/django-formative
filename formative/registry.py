from collections import Container, Iterable, Sized
from django.utils.encoding import python_2_unicode_compatible
from django.utils import six
from django.utils.functional import cached_property
from django.utils.text import camel_case_to_spaces
from formative.exceptions import FormativeTypeNotRegistered
from formative.utils import formative_form_factory


class FormativeTypeBase(type):
    def __new__(mcs, name, bases, attrs):
        if 'name' not in attrs:
            attrs['name'] = camel_case_to_spaces(name).lower()
        if 'verbose_name' not in attrs:
            attrs['verbose_name'] = attrs['name'].title()
        if 'fieldsets' not in attrs:
            attrs['fieldsets'] = None
        return super(FormativeTypeBase, mcs).__new__(mcs, name, bases, attrs)


@python_2_unicode_compatible
@six.add_metaclass(FormativeTypeBase)
class FormativeType(object):
    def __init__(self, model):
        self.model = model

    @cached_property
    def form(self):
        return self.get_form()

    def get_form(self, exclude=None):
        form = formative_form_factory(
            self.model, self.form_class, exclude=exclude)
        form.formative_type = self
        return form

    def __str__(self):
        return self.verbose_name


class FormativeTypeRegistry(Sized, Iterable, Container):
    """
    Formative type registry
    """
    def __init__(self):
        self.__registry = {}

    def __contains__(self, name):
        return name in self.__registry

    def __iter__(self):
        for key, value in sorted(self.__registry.items()):
            yield value

    def __len__(self):
        return len(self.__registry)

    def register(self, cls, model):
        """
        Register a type
        """
        self.__registry[cls.name] = cls(model)

    def get(self, name):
        """
        Get a type from the registry using its name.
        Raises FormativeTypeNotRegistered if the name is not found in the
        registry.
        """
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
