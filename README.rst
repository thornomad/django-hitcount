Django-HitCount
===============

.. image:: https://travis-ci.org/thornomad/django-hitcount.svg?branch=master
    :target: https://travis-ci.org/thornomad/django-hitcount
.. image:: https://coveralls.io/repos/thornomad/django-hitcount/badge.svg?branch=master
    :target: https://coveralls.io/r/thornomad/django-hitcount?branch=master

Basic app that allows you to track the number of hits/views for a particular object.  Full documentation is available at: http://django-hitcount.rtfd.org

Example Project:
----------------

I have added an example project with a simple Blog application so you can see the hit counting demonstrated.  You can use that to test the functionality and it should work out of the box with Django 1.8.1 and Python 2.7.x.

You can load some initial fixtures at::

    python manage.py migrate          # will load some data fixtures for you
    python manage.py createsuperuser  # if you want admin access

Settings:
---------

Be sure to add this to your `settings.py`::

   SESSION_SAVE_EVERY_REQUEST = True

TODO
-----

* More tests! (low coverage)
* Internationalization (although this has been started)
* Port to python 3.x
* Upload to pip repository

Additional Authors and Thanks
-----------------------------

This doesn't include everyone and if I missed someone let me know I will add it.

Thanks goes to:

 * Basil Shubin and his work at <https:/github.com/bashu/django-hitcount-headless>
 * ariddell for putting the `setup.py` package together

