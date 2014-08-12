from UserDict import UserDict

_registry = set()


class FormativeType(object):
    def __init__(self, name, form=None, verbose_name=None):
        self.name = name
        self.verbose_name = verbose_name or name.title()
        self.form = form

    def set_formative_type(self, form):
        if form.formative_type != self.name:
            form.formative_type = self.name
        return form

    def get_form(self):
        return self.set_formative_type(self.form)

    def __unicode__(self):
        return self.verbose_name


class FormativeTypeRegistry(UserDict):
    def __init__(self):
        self.data = {}
        for formative_type in _registry:
            self.data[formative_type.name] = formative_type


def register(definition):
    _registry.add(definition)
