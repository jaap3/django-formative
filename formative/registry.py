from collections import Mapping
from django.utils.encoding import python_2_unicode_compatible
from formative.exceptions import FormativeTypeNotRegistered

_registry = {}


@python_2_unicode_compatible
class FormativeType(object):
    def __init__(self, name, form, fieldsets=None, verbose_name=None):
        self._form = None
        self.name = name
        self.form = form
        self.fieldsets = fieldsets
        self.verbose_name = verbose_name or name.title()

    @property
    def form(self):
        # Set type in the getter because a form may be registered twice
        return self._set_formative_type(self._form)

    @form.setter
    def form(self, form):
        self._form = form

    def _set_formative_type(self, form):
        form.formative_type = self
        return form

    def get_form(self, request, obj=None, **kwargs):
        """
        Helper method for the admin, works like ModelAdmin.get_form
        """
        return self.form

    def get_fieldsets(self, request, obj=None, **kwargs):
        """
        Helper method for the admin, works like ModelAdmin.get_fieldsets
        """
        return self.fieldsets

    def __str__(self):
        return self.verbose_name


class FormativeTypeRegistry(Mapping):
    def __iter__(self):
        for formative_type in _registry.keys():
            yield formative_type

    def __getitem__(self, item):
        if item in _registry:
            return _registry[item]
        raise FormativeTypeNotRegistered

    def __len__(self):
        return len(_registry)


def register(name, form, fieldsets=None, verbose_name=None, cls=FormativeType):
    _registry[name] = cls(
        name, form, fieldsets=fieldsets, verbose_name=verbose_name)


def autodiscover():
    """
    Auto-discover INSTALLED_APPS formative_forms.py modules and fail silently
    if not present.
    """
    from django.conf import settings
    from django.utils.importlib import import_module
    from django.utils.module_loading import module_has_submodule

    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        # Attempt to import the app's formative module.
        try:
            import_module('%s.formative_forms' % app)
        except:
            # Decide whether to bubble up this error. If the app just
            # doesn't have an formative module, we can ignore the error
            # attempting to import it, otherwise we want it to bubble up.
            if module_has_submodule(mod, 'formative_forms'):
                raise  # pragma: nocover
