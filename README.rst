==============
django-backend
==============

Installation
============

Add the following apps to your ``INSTALLED_APPS`` settings:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.staticfiles',
        ...
        'django_backend',
        'django_ajax',
        'django_assets',
        'floppyforms',
    )

 Add the following line to your ``urls.py``:

 .. code-block:: python

    url(r'^backend/', include(django_backend.site.get_urls(), namespace='django_backend')),

TODO: continue, propably not complete yet
