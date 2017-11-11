Installation and Usage
======================

Install django-hitcount::

    pip install django-hitcount

Add django-hitcount to your ``INSTALLED_APPS``::

    # settings.py
    INSTALLED_APPS = (
        ...
        'hitcount'
    )

View the :doc:`additional settings section </settings>` for a list of the django-hitcount settings that are available.

For a working implementation, you can view the `example project`_ on Github.

Counting Hits
-------------

The main business-logic for evaluating and counting a `Hit` is done in ``hitcount.views.HitCountMixin.hit_count()``.  You can use this class method directly in your own Views or you can use one of the Views packaged with this app.

 * `HitCountJSONView`_: a JavaScript implementation which moves the business-logic to an Ajax View and hopefully speeds up page load times and eliminates some bot-traffic
 * `HitCountDetailView`_: which provides a wrapper from  Django's generic ``DetailView`` and allows you to process the Hit as the view is loaded

HitCountMixin
^^^^^^^^^^^^^

This mixin can be used in your own class-based views or you can call the ``hit_count()`` class method directly.   The method takes two arguments, a ``HttpRequest`` and ``HitCount`` object it will return a namedtuple: ``UpdateHitCountResponse(hit_counted=Boolean, hit_message='Message')``.  ``hit_counted`` will be ``True`` if the hit was counted and ``False`` if it was not.  ``hit_message`` will indicate by what means the Hit was either counted or ignored.

It works like this. ::

    from hitcount.models import HitCount
    from hitcount.views import HitCountMixin

    # first get the related HitCount object for your model object
    hit_count = HitCount.objects.get_for_object(your_model_object)

    # next, you can attempt to count a hit and get the response
    # you need to pass it the request object as well
    hit_count_response = HitCountMixin.hit_count(request, hit_count)

    # your response could look like this:
    # UpdateHitCountResponse(hit_counted=True, hit_message='Hit counted: session key')
    # UpdateHitCountResponse(hit_counted=False, hit_message='Not counted: session key has active hit')

To see this in action see the `views`_.py code.

HitCountJSONView
^^^^^^^^^^^^^^^^

The ``hitcount.views.HitCountJSONView`` can be used to handle an AJAX POST request.  Django-hitcount comes with a bundled `jQuery plugin`_ for speeding up the ``$.post`` process by handling the retrieval of the CSRF token for you.

If you wish to use the ``HitCountJSONView`` in your project you first need to update your ``urls.py`` file to include the following::

    # urls.py
    urlpatterns = [
        ...
        url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    ]

Next, you will need to add the JavaScript Ajax request to your template.  To do this, use the ``{% get_hit_count_js_variables for post as [var_name] %}`` template tag to get the ``ajax_url`` and ``hitcount_pk`` for your object.  The ``hitcount_pk`` is needed for POST-ing to the ``HitCountJSONView``.

Here is an example of how all this might work together with the bundled `jQuery plugin`_.  It is taken from the `example project`_ and the jQuery can be modified to suit your needs.  In the example below it simply updates the template with the ``HitCountJSONView`` response after the Ajax call is complete.

::

    {% load staticfiles %}
    <script src="{% static 'hitcount/jquery.postcsrf.js' %}"></script>

    {% load hitcount_tags %}
    {% get_hit_count_js_variables for post as hitcount %}
    <script type="text/javascript">
    jQuery(document).ready(function($) {
      // use the template tags in our JavaScript call
      $.postCSRF("{{ hitcount.ajax_url }}", { hitcountPK : "{{ hitcount.pk }}" })
        .done(function(data){
          $('<i />').text(data.hit_counted).attr('id','hit-counted-value').appendTo('#hit-counted');
          $('#hit-response').text(data.hit_message);
      }).fail(function(data){
          console.log('POST failed');
          console.log(data);
      });
    });
    </script>

HitCountDetailView
^^^^^^^^^^^^^^^^^^

The ``HitCountDetailView`` can be used to do the business-logic of counting the hits by setting ``count_hit=True``.  See the `views`_ section for more information about what else is added to the template context with this view.

Here is an example implementation from the `example project`_::

    from hitcount.views import HitCountDetailView

    class PostCountHitDetailView(HitCountDetailView):
        model = Post        # your model goes here
        count_hit = True    # set to True if you want it to try and count the hit

.. note:: Unlike the JavaScript implementation (above), this View will do all the HitCount processing *before* the content is delivered to the user; if you have a large dataset of Hits or exclusions, this could slow down page load times.  It will also be triggered by web crawlers and other bots that may not have otherwise executed the JavaScript.

Displaying Hits
---------------

There are different methods for *displaying* hits:

* `Template Tags`_: provide a robust way to get related counts
* `Views`_: allows you to wrap a class-based view and inject additional context into your template
* `Models`_: can have a generic relation to their respective ``HitCount``

Template Tags
^^^^^^^^^^^^^

For a more granular approach to viewing the hits for a related object you can use the ``get_hit_count`` template tag.

::

    # remember to load the tags first
    {% load hitcount_tags %}

    # Return total hits for an object:
    {% get_hit_count for [object] %}

    # Get total hits for an object as a specified variable:
    {% get_hit_count for [object] as [var] %}

    # Get total hits for an object over a certain time period:
    {% get_hit_count for [object] within ["days=1,minutes=30"] %}

    # Get total hits for an object over a certain time period as a variable:
    {% get_hit_count for [object] within ["days=1,minutes=30"] as [var] %}

Views
^^^^^

The ``hitcount.views.HitCountDetailView`` extends Django's generic ``DetailView`` and injects an additional context variable ``hitcount``.

::

    {# the primary key for the hitcount object #}
    {{ hitcount.pk }}

    {# the total hits for the object #}
    {{ hitcount.total_hits }}

If you have set ``count_hit=True`` (see: `HitCountDetailView`_) two additional variables will be set.

::

    {# whether or not the hit for this request was counted (true/false) #}
    {{ hitcount.hit_counted }}

    {# the message form the UpdateHitCountResponse #}
    {{ hitcount.hit_message }}


Models
^^^^^^

.. note:: You are not *required* to do anything specific with your models; django-hitcount relies on a ``GenericForeignKey`` to create the relationship to your model's ``HitCount``.

If you would like to add a reverse lookup in your own model to its related ``HitCount`` you can utilize the ``hitcount.models.HitCountMixin``.

::

    from django.db import models

    from hitcount.models import HitCountMixin

    # here is an example model with a GenericRelation
    class MyModel(models.Model, HitCountMixin):

      # adding a generic relationship makes sorting by Hits possible:
      # MyModel.objects.order_by("hit_count_generic__hits")
      hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # you would access your hit_count like so:
    my_model = MyModel.objects.get(pk=1)
    my_model.hit_count.hits                 # total number of hits
    my_model.hit_count.hits_in_last(days=7) # number of hits in last seven days


.. _jQuery plugin: https://github.com/thornomad/django-hitcount/blob/master/hitcount/static/hitcount/jquery.postcsrf.js

.. _example project: https://github.com/thornomad/django-hitcount/tree/master/example_project

.. _views: https://github.com/thornomad/django-hitcount/blob/master/hitcount/views.py
