from collections import Mapping

_registry = set()


class FormativeType(object):
    def __init__(self, name, form, fieldsets=None, verbose_name=None):
        self.name = name
        self.form = form
        self.fieldsets = fieldsets
        self.verbose_name = verbose_name or name.title()

    @property
    def form(self):
        return self._set_formative_type(self._form)

    @form.setter
    def form(self, form):
        self._form = form

    def _set_formative_type(self, form):
        form.formative_type = self.name
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
        for formative_type in _registry:
            yield formative_type.name

    def __getitem__(self, item):
        for formative_type in _registry:
            if formative_type.name == item:
                return formative_type
        raise KeyError

    def __len__(self):
        return len(_registry)


def register(name, form, fieldsets=None, verbose_name=None, cls=FormativeType):
    _registry.add(cls(name, form, fieldsets=fieldsets,
                      verbose_name=verbose_name))


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
                raise
