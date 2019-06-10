Changelog
=========

Version 1.3.1
-------------

 * fixed ValueError: invalid literal for int() with base 10 `#64`_

Version 1.3.0
-------------

 * Django 2.x support (@stasfilin) `#67`_

Version 1.2.4
-------------

 * improved querying speed of `hitcount_cleanup` (@dulacp) `#66`_

Version 1.2.3
-------------

 * added indexing to `Hit.ip` and `Hit.session` (@maxg0) `#63`_
 * removed testing support for python 3.3

Version 1.2.2
-------------

 * added ``on_delete=models.CASCADE`` and test (will be required in version 2.0) `#47`_
 * removed ``b`` (bytes) flag from _initial_ migration `#48`_
 * removed testing support for python 3.2

Version 1.2.1
-------------

 * fixed system check error in Django 1.9 - `#43`_

Version 1.2
-----------

 * added ``hitcount.models.HitCountMixin`` to provide a reverse lookup property to a model's ``HitCount``
 * deprecated ``hitcount.views_update_hit_count()`` and moved the business logic into ``hitcount.views.HitCountMixin.hit_count()``
 * deprecated ``hitcount.views.update_hit_count_ajax()`` and replaced with class-based view ``hitcount.views.HitCountJSONView``
 * deprecated ``static/hitcount-jquery.js`` and replaced with ``static/jquery.postcsrf.js`` (a more generic way to handle the Ajax POST CSRF fun-party)
 * updated Django and Python version testing/support (>=1.7 as of Oct 2015)
 * updated example_project to use new views and jQuery plugin
 * updated tests to rely on the example_project

Version 1.1.1
-------------

 * fixed ``session_key`` returning ``None`` - `#40`_ (>=1.8.4)
 * removed requirement for `SESSION_SAVE_EVERY_REQUEST`
 * removed `patterns` for urls.py (>=1.9)
 * updated management command, using ``BaseCommand`` instead of ``NoArgsCommand`` (>=1.9)
 * added ``TEMPLATES`` to `conftest.py`

Version 1.1.0
-------------

 * added tests (lots of them)
 * added documentation
 * support for Django 1.4.x - 1.8.x
 * support for Python 3.x
 * created an example project
 * squashed bugs
 * released to pip
 * more, I'm sure!

.. note:: if you are upgrading from version 0.2 (it's so old!) the ``HitCount.object_pk`` was changed from a ``CharField`` to a ``PositiveIntegerField``.  You will have to manually fix this in your database after upgrading.

.. _#64: https://github.com/thornomad/django-hitcount/issues/64
.. _#67: https://github.com/thornomad/django-hitcount/pull/67
.. _#63: https://github.com/thornomad/django-hitcount/issues/63
.. _#40: https://github.com/thornomad/django-hitcount/issues/40
.. _#43: https://github.com/thornomad/django-hitcount/issues/43
.. _#47: https://github.com/thornomad/django-hitcount/issues/47
.. _#48: https://github.com/thornomad/django-hitcount/pull/48
.. _#66: https://github.com/thornomad/django-hitcount/pull/66
