Basic example
=============

This basic examples shows you how to register a backend, create a filter form
for one and how to customize the columns in the list view of a backend.

The hotspots of this example are in:

- Defining the backends happens in ``project/blog/backend.py``.
- The base site is hooked up into the url config in ``project/urls.py``.

Get started
-----------

- Clone the django_backend repository
- cd into the root of the repository
- Create a virtualenv and activate it
- Run these commands::

    pip install "Django==1.8.12"
    pip install -e .

Now the example is ready to use, you can start it by running::

    cd examples/basic_example
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

Now visit the backend at `http://localhost:8000/backend/ <backend_url>` and log
in with the credentials you have entered during the ``createsuperuser``
command.

.. _backend_url: http://localhost:8000/backend/
