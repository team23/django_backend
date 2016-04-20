A blogging app
==============

This example contains a simple blogging app where we use django_backend to
provide the editorial interface.

The blogging app has the following characteristics:

- There are authors who have a name.
- There are post that have a title, a content text, and an author associated.
- The posts have a pub date that controls if they are visible in the frontend.

This example only contains the backend code. To keep it simple we don't include
any frontend code to display the posts.

In this example you see the following features of django_backend in use:

In ``project/blog/backend.py`` you can see ...

- … how we define a custom backend for ``Post``
- … how we define a filter form for the post backend
- … how we define custom list columns for the post backend
- … how we add a custom view to the post backend
- … how we define an inline backend for ``Author``
- … how we use a group to display the backends in the backend sidebar

Also have a look in ``project/urls.py`` to see how we hook up the urls in the
project.

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

Now visit the backend at `http://localhost:8000/backend/ <backend_url>`_ and
log in with the credentials you have entered during the ``createsuperuser``
command.

.. _backend_url: http://localhost:8000/backend/
