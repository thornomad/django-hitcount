Installation and Usage
======================

Install django-hitcount by running::

    pip install -e git://github.com/thornomad/django-hitcount.git#egg=django-hitcount

Edit your ``settings.py`` file and add django-hitcount to your installed apps, as well as enabling ``SESSION_SAVE_EVERY_REQUEST``::

    # settings.py

    INSTALLED_APPS = (
        ...
        'hitcount'
    )

    # needed for django-hitcount to function
    SESSION_SAVE_EVERY_REQUEST = True

In your ``urls.py`` file add the following::

    # urls.py
    urlpatterns = patterns('',
        ...
        url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    )

View the :doc:`additional settings section </settings>` for more information.

Template Tags
-------------

Django-Hitcount is designed to use Ajax to record the ``Hits`` to an object.  There is an `example jQuery`_ implementation that demonstrates how this might work along with some template tags to assist in embedding the necessary javascript information.  View the `example project`_ for a working demonstration.

Start by loading hitcount tags on the desired templates::

    {% load hitcount_tags %}

Recording a Hit
^^^^^^^^^^^^^^^

If you want to use the `example jQuery`_ script on your project, you can add it like so::

    {% load staticfiles %}
    <script src="{% static 'hitcount/hitcount-jquery.js' %}"></script>

Then, on your object detail page you inject the needed javascript variables::

    # use default insertion method for hitcount-jquery.js:
    {% insert_hit_count_js_variables for object %}

    # OR: use a template variable to inject as you see fit
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

.. _example jQuery: https://github.com/thornomad/django-hitcount/blob/master/hitcount/static/hitcount/hitcount-jquery.js

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project
