==============
django-backend
==============

|pypi-badge| |build-status|

.. note::

    This module can be imported in python with the name ``django_backend``. The
    PyPI package is called `django-admin-backend`_ though. We had to use a
    different name as ``django-backend`` was already registered on PyPI. It's a
    little unfortunate this way, but a necessary workaround for now.

.. _django-admin-backend: https://pypi.python.org/pypi/django-admin-backend

Installation
============

Add the following apps to your ``INSTALLED_APPS`` settings:

.. code:: python

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        ...
        'django_backend',
        'floppyforms',
    )

Make sure ``SITE_ID`` is set:

.. code:: python

    SITE_ID = 1

Make sure ``LANGUAGE_CODE`` is valid:

.. code:: python

    LANGUAGE_CODE = 'en'

**Warning:** Django's default language code is *not* valid, as "en-us" is not included in settings.LANGUAGES.

Add the following line to your ``urls.py``:

.. code:: python

    url(r'^backend/', include(django_backend.site.get_urls(), namespace='django_backend')),

TODO: continue, propably not complete yet

Development
===========

Run tests
---------

.. code:: bash

    # Set everything up. You want to do this in a virtualenv.
    pip install -r tests/requirements.txt
    python setup.py develop

    # Run the tests. Should be executed in the root of the project.
    py.test

.. |build-status| image:: https://travis-ci.org/team23/django_backend.svg
    :target: https://travis-ci.org/team23/django_backend

.. |pypi-badge| image:: https://img.shields.io/pypi/v/django-admin-backend.svg
    :target: https://pypi.python.org/pypi/django-admin-backend

Build static assets
-------------------

.. code:: bash

    npm install
    gulp build

    # Use gulp watch to continuously build on source file changes.
    gulp watch

Or to create a development build that includes source maps, execute the ``dev`` task first, like:

.. code:: bash

    gulp dev build
