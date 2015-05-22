django-hitcount
================

django-hitcount allows you to track the number of hits/views for a particular object.

.. toctree::
   :hidden:

   index
   settings

Installation
------------

Install django-hitcount by running::

    pip install -e git://github.com/thornomad/django-hitcount.git#egg=django-hitcount

Add django-hitcount to your installed apps::

    INSTALLED_APPS = (
        # ...
        'hitcount'
    )

And add the following line to your `settings.py` file::

    SESSION_SAVE_EVERY_REQUEST = True

View the :doc:`additional settings section </settings>` for more information.

Template Tag Usage
------------------

django-hitcount is designed to use Ajax to record the ``Hits`` to an object.  There is an `example jQuery`_ implementation that demonstrates how this might work along with some template tags to assist in embedding the necessary javascript information.  View the `example project`_ for a working demonstration.

Start by loading hitcount tags on the desired templates::

    {% load hitcount_tags %}

Recording a Hit
^^^^^^^^^^^^^^^

If you want to use the `example jQuery`_ on your project, you can add it like so::

    {% load staticfiles %}
    <script src="{% static 'hitcount/hitcount-jquery.js' %}"></script>

Then, on your object detail page (or similar) you inject the needed javascript variables::

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

Example Project
---------------

If you download the source from GitHub there is an `example project`_ that should demonstrate the functionality out-of-the-box (using javascript).::

    $ cd example_project
    $ python manage.py migrate          # will load some data fixtures for you
    $ python manage.py createsuperuser  # for access to the admin portion

Issues
------

Use the GitHub `issue tracker`_ for django-hitcount to submit bugs, issues, and feature requests.

Contributing
------------

To contribute to django-hitcount first pleast `create a fork`_ on GitHub, then clone your fork, make some changes, and submit a pull request.

.. _issue tracker: https://github.com/thornomad/django-hitcount/issues

.. _create a fork: https://github.com/thornomad/django-hitcount

.. _example jQuery: https://github.com/thornomad/django-hitcount/blob/master/hitcount/static/hitcount/hitcount-jquery.js

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project
