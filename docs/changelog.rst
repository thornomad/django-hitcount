Changelog
=========

Version 1.1.1:
--------------

 * fixed ``session_key`` returning ``None`` `#40`_ (>=1.8.4)
 * removed requirement for `SESSION_SAVE_EVERY_REQUEST`
 * removed `patterns` for urls.py (>=1.9)
 * updated management command, using ``BaseCommand`` instead of ``NoArgsCommand`` (>=1.9)
 * added ``TEMPLATES`` to `conftest.py`

Version 1.1.0:
--------------

 * added tests (lots of them)
 * added documentation
 * support for Django 1.4.x - 1.8.x
 * support for Python 3.x
 * created an example project
 * squashed bugs
 * released to pip
 * more, I'm sure!


.. _#40: https://github.com/thornomad/django-hitcount/issues/40
