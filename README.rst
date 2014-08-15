=============================
django-formative
=============================

.. image:: https://badge.fury.io/py/django-formative.png
    :target: https://badge.fury.io/py/django-formative

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
