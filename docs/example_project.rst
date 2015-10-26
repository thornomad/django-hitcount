Example Project
===============

There is an `example project`_ the demonstrates the functionality of this app.  It's fairly easy to get this working using the Django development server.  Be sure to run this inside your own ``virtualenv`` (but who doesn't, these days?!). ::

    $ git clone git@github.com:thornomad/django-hitcount.git
    $ cd django-hitcount/example_project
    $ pip install -r requirements.txt   # sqlite requires pytz
    $ python manage.py migrate          # will load some data fixtures for you
    $ python manage.py createsuperuser  # for access to the admin portion
    $ python manage.py runserver        # should be all set!

When you are ready to work on your own site, check out the :doc:`installation` and :doc:`settings` sections.

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project
