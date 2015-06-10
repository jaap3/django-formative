=============================
django-formative
=============================

.. .. image:: https://pypip.in/version/django-formative/badge.svg
      :target: https://pypi.python.org/pypi/django-formative/
      :alt: Latest Version

.. image:: https://travis-ci.org/jaap3/django-formative.png?branch=master
    :target: https://travis-ci.org/jaap3/django-formative

.. image:: https://coveralls.io/repos/jaap3/django-formative/badge.png?branch=master
    :target: https://coveralls.io/r/jaap3/django-formative?branch=master

Flexible non-model data objects in Django's admin using Django forms.


Quickstart
----------

Install django-formative::

    pip install django-formative

Then add it to your Django project's ``INSTALLED_APPS``::

    INSTALLED_APPS += 'formative'

Run ``syncdb`` or ``migrate`` to get the database up to date.


Formative Types
---------------

Now it's time to define a *formative type*. Create a file called
``formative_types.py`` in a app that's in the ``INSTALLED_APPS`` list.
In this file you can define forms and register them with formative::

    from django import forms
    from formative.forms import FormativeForm
    from formative.models import FormativeBlob
    from formative.registry import FormativeType

    class SimpleForm(FormativeForm):
        name = forms.CharField()
        body = forms.CharField(widget=forms.Textarea)

    class SimpleType(FormativeType):
        form_class = SimpleForm

    FormativeBlob.register(SimpleType)

Then add the following to your project's ``urls.py``, right next to
the call to ``admin.autodiscover()``::

    import formative
    formative.autodiscover()

That's it. Now you can create formative objects in the admin using your
simple form.


Inline Formative Types
----------------------

You can also associate formative data with other models. Register the types
you want to use with the ``InlineFormativeBlob`` model::

    from formative.models import InlineFormativeBlob

    InlineFormativeBlob.register(SimpleType)

Then use the ``InlineFormativeBlobAdmin`` and ``FormativeBlobInline`` for the
model's admin class::

    from django.contrib import admin
    from formative.admin import InlineFormativeBlobAdmin, FormativeBlobInline
    from yourproject.models import Book

    class BookAdmin(InlineFormativeBlobAdmin):
        inlines = [FormativeBlobInline]

    admin.site.register(Book, BookAdmin)

You'll now be able to add formative objects to ``Book`` instances.


Using formative data
--------------------

You probably want to use the data in some way. Simply get an instance of
a FormativeBlob by its ``unique_identifier`` and access the data property as
a dictionary::

    from formative.models import FormativeBlob
    >>> f = FormativeBlob.objects.get(unique_identifier='simple')
    >>> f.unique_identifier
    'simple'
    >>> f.data['name']
    'test'


Template tags
-------------

Django-formative also provides a templatetag to use the data in your templates::

    {% load formative_tags %}
    {% get_blob 'simple' as simple %}
    {{ simple.unique_identifier }}
    {{ simple.data.name }}
    {{ simple.data.body }}
