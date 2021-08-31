Overview
========

Django-Hitcount allows you to track the number of hits (views) for a particular object. This isn’t meant to be a full-fledged tracking application or a real analytic tool; it's just a basic hit counter.

How one tracks a "hit" or "view" of a web page is not such a simple thing as it might seem.  That's why folks rely on Google Analytics or similar tools.  It's tough!  This is a simple app with some settings and features that should suit the basic needs of smaller sites.

It comes ready to track hits with a ``HitCountDetailView`` and a ``HitCountJSONView`` (to use the out-of-the-box JavaScript method, you will need jQuery -- although writing your own JavaScript implementation is not hard).

Requirements and Compatibility
------------------------------

The 1.2.x series currently supports Django >= 1.8.x and those versions of Python also supported by Django (including Python 3).  Development of django-hitcount follows Django's `supported versions release schedule`_ and testing for older versions of Django/Python will be removed as time marches on.

.. note:: If you are running a Django 1.4, 1.5, or 1.6 stick with the django-hitcount v1.1.1.  If you are running a Django version pre-1.4 you can try django-hitcount v0.2 (good luck!).

.. _supported versions release schedule: https://www.djangoproject.com/download/#supported-versions
