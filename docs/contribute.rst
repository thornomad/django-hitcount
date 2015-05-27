Contribution and Testing
======================

I would love to make it better.  Please fork, branch, and push.  Next up, in my mind, is full testing coverage; then: python 3.x series.  After that, I'd like to implement a way to link HitCounts to objects without relying on the generic content types.

Testing
-------

You can run the tests by installing the requirements and then executing ``runtests.py``::

    $ pip install -r tests/requirements.txt
    $ ./runtests.py

This method using ``py.test`` for test discovery (so older versions of Django can find all the tests).  If you would like to use Django's own test runner you can execute::

    $ ./runtests.py --django


