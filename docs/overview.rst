Overview
========

Django-Hitcount allows you to track the number of hits (views) for a particular object. This isn’t meant to be a full-fledged tracking application or a real analytic tool; it's just a basic hit counter.

.. warning::

May/June 2015: I bumped the version to the 1.x series because I am actively working on bringing the project up to speed (tests, python 3.x, and internal upgrades).  I am still not finished with all the work -- when complete, it will be released as a ``pip`` package.

Requirements and Compatibility
------------------------------

Currently supporting versions 2.6 and 2.7 of Python.  Django >= 1.4.

Example Project
---------------

If you would like to see how this works there is an `example project`_ included on the GitHub repository that should demonstrate the functionality out-of-the-box (`using javascript`_).  Of course, recommending you install this in a virtual environment.::

    $ git clone git@github.com:thornomad/django-hitcount.git
    $ cd django-hitcount/example_project
    $ pip install -r requirements.txt   # sqlite requires pytz
    $ python manage.py migrate          # will load some data fixtures for you
    $ python manage.py createsuperuser  # for access to the admin portion
    $ python manage.py runserver        # should be all set!

You can run the server and visit the admin and see it all in action.  When you are ready to work on your own site, check out the :doc:`installation` and :doc:`settings` sections.

.. _using javascript: https://github.com/thornomad/django-hitcount/blob/master/hitcount/static/hitcount/hitcount-jquery.js

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project
