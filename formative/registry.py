from UserDict import UserDict

_registry = set()


class FormativeType(object):
    def __init__(self, name, form=None, verbose_name=None):
        self.name = name
        self.form = self._set_formative_type(form)
        self.verbose_name = verbose_name or name.title()

    def _set_formative_type(self, form):
        form.formative_type = self.name
        return form

    def get_form(self, request, obj=None, **kwargs):
        """
        Helper method for the admin, works like ModelAdmin.get_form
        """
        return self.form

    def __unicode__(self):
        return self.verbose_name


class FormativeTypeRegistry(UserDict):
    def __init__(self):
        self.data = {}
        for formative_type in _registry:
            self.data[formative_type.name] = formative_type


def register(definition):
    _registry.add(definition)
