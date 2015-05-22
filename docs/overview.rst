Overview
========

Django-Hitcount allows you to track the number of hits/views for a particular object. This isn’t meant to be a full-fledged tracking application (see django-tracking) or a real analytic tool (try Google Analytics); rather, it’s meant to  count the number of hits/view on an object-per-object basis.

Example Project
---------------

If you would like to see how this works there is an `example project`_ included on the GitHub repository that should demonstrate the functionality out-of-the-box (using javascript).  Download everything from github and then run::

    $ cd example_project
    $ python manage.py migrate          # will load some data fixtures for you
    $ python manage.py createsuperuser  # for access to the admin portion

You can run the server and visit the admin and see it all in action.  When you are ready to work on your own site, check out the :doc:`installation` and :doc:`settings` sections.

.. _example jQuery: https://github.com/thornomad/django-hitcount/blob/master/hitcount/static/hitcount/hitcount-jquery.js

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project
