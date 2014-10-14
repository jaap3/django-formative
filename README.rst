=============================
django-formative
=============================

.. image:: https://pypip.in/version/django-formative/badge.svg
    :target: https://pypi.python.org/pypi/django-formative/
    :alt: Latest Version

.. image:: https://travis-ci.org/jaap3/django-formative.png?branch=master
    :target: https://travis-ci.org/jaap3/django-formative

.. image:: https://coveralls.io/repos/jaap3/django-formative/badge.png?branch=master
    :target: https://coveralls.io/r/jaap3/django-formative?branch=master

Flexible non-model data objects in Django's admin using Django forms.

Documentation
-------------

The full documentation is at https://django-formative.readthedocs.org.

Quickstart
----------

Install django-formative::

    pip install django-formative

Then add it to your Django project's `INSTALLED_APPS`::

    INSTALLED_APPS += 'formative'

Run `syncdb` or `migrate` to get the database up to date.

Now it's time to define a *formative type*. Create a file called
`formative_forms.py` in a app that's in the `INSTALLED_APPS` list.
In this file you can define forms and register them with formative::

    import formative
    from django import forms
    from formative.forms import FormativeBlobForm


    class SimpleForm(FormativeBlobForm):
        name = forms.CharField()
        body = forms.CharField(widget=forms.Textarea)


    formative.register('simple', SimpleForm)

Then add the following to your project's `urls.py`, right next to
the call to `admin.autodiscover()`::

    import formative
    formative.autodiscover()

That's it. Now you can create formative objects in the admin using your
simple form.

You probably want to use the data in some way. Simply get an instance of
a FormativeBlob by its unique_identifier and access the data property as
a dictionary::

    from formative.models import FormativeBlob
    >>> f = FormativeBlob.objects.get(unique_identifier='simple')
    >>> f.unique_identifier
    'simple'
    >>> f.data['name']
    'test'

Django-formative also provides a templatetag to use the data in your templates::

    {% load formative_tags %}
    {% get_formative_blob 'simple' as simple %}
    {{ simple.unique_identifier }}
    {{ simple.data.name }}
    {{ simple.data.body }}
