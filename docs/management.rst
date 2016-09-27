Management Commands
===================

By default, your ``Hits`` remain in the database indefinitely.  If you would like to periodically prune your stale ``Hits`` you can do so by running the the management command ``hitcount_cleanup``.::

     ./manage.py hitcount_cleanup

The command relies on the setting ``HITCOUNT_KEEP_HIT_IN_DATABASE`` to determine how far back to prune.  See the :doc:`additional settings section </settings>` for more information.
