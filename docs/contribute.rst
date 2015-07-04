Contribution and Testing
======================

I would love to make it better.  Please fork, branch, and push.  I plan to do my work in the ``develop`` branch before moving it to ``master`` for a real release.  You can safely ignore the ``devel`` branch which is old and stale but has something in it I can't remember why I'm saving.

Testing
-------

You can run the tests by installing the requirements and then executing ``runtests.py``::

    $ pip install -r tests/requirements.txt
    $ ./runtests.py

This method using ``py.test`` for test discovery (so older versions of Django can find all the tests).  If you would like to use Django's own test runner you can execute::

    $ ./runtests.py --django
