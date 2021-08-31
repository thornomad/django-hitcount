Contribution and Testing
========================

I would love to make it better.  Please fork, branch, and push.

Please make new features/improvements against the develop branch.  If you are patching a bug or providing a fix of some sort that can be made against the master branch.  For larger features, please create your own feature branch first before you make the pull request.

.. note:: You can safely ignore the ``devel`` branch which is old and stale but has something in it I can't remember why I'm saving it.  Call me a hoarder.

Testing
-------

You can run the tests by installing the requirements and then executing ``runtests.py``::

    $ pip install -r tests/requirements.txt
    $ ./runtests.py     # against your currently installed version of Django
    $ tox               # against the entire array of Django/Python versions

This method using ``py.test`` for test discovery and will also run `flake8` for code formatting.  If you would like to use Django's own test runner you can execute::

    $ ./runtests.py --django
