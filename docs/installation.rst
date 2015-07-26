Installation and Usage
======================

For a working implementation, you can view the `example project`_ on Github.

Install django-hitcount::

    pip install django-hitcount

Settings.py
-----------

Add django-hitcount to your ``INSTALLED_APPS``, enable ``SESSION_SAVE_EVERY_REQUEST``::

    # settings.py

    INSTALLED_APPS = (
        ...
        'hitcount'
    )

    # needed for django-hitcount to function properly
    SESSION_SAVE_EVERY_REQUEST = True

Urls.py
-------
In your ``urls.py`` file add the following::

    # urls.py
    urlpatterns = patterns('',
        ...
        url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    )

View the :doc:`additional settings section </settings>` for more information.

Template Magic
--------------

Django-hitcount comes packaged with a `jQuery implementation`_ that works out-of-the-box to record the ``Hits`` to an object (be it a blog post, poll, etc).  To use the `jQuery implementation`_ you can either include the app's script file (as the documentation below shows) or to copy-paste the script into your own jQuery code.  Of course: you could also implement this without relying on jQuery.

Start by loading hitcount tags on the desired templates::

    {% load hitcount_tags %}

Recording a Hit
^^^^^^^^^^^^^^^

If you want to use the `jQuery implementation`_ in your project, you can add the Javascript file to your template like so::

    {% load staticfiles %}
    <script src="//code.jquery.com/jquery-1.11.3.min.js"></script>
    <script src="{% static 'hitcount/hitcount-jquery.js' %}"></script>

Then, on your object detail page (blog, page, poll, etc) you inject the needed javascript variables::

    # use default insertion method for hitcount-jquery.js:
    {% insert_hit_count_js_variables for object %}

    # or you can use a template variable to inject as you see fit
    {% get_hit_count_js_variables for object as hitcount %}
    ({ hitcount.ajax_url }}
    {{ hitcount.pk }}

Displaying Hit Information
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can retrieve the number of hits for an object many different ways::

    # Return total hits for an object:
    {% get_hit_count for [object] %}

    # Get total hits for an object as a specified variable:
    {% get_hit_count for [object] as [var] %}

    # Get total hits for an object over a certain time period:
    {% get_hit_count for [object] within ["days=1,minutes=30"] %}

    # Get total hits for an object over a certain time period as a variable:
    {% get_hit_count for [object] within ["days=1,minutes=30"] as [var] %}

.. _jQuery implementation: https://github.com/thornomad/django-hitcount/blob/master/hitcount/static/hitcount/hitcount-jquery.js

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project
