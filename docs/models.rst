Models
======

.. note:: You are not *required* to do anything specific with your models; django-hitcount relies on a ``GenericForeignKey`` to create the relationship to your model's ``HitCount``.

If you would like to add a reverse lookup in your own model to its related ``HitCount`` you can utilize the ``hitcount.models.HitCountMixin``.

::

    from django.db import models

    from hitcount.models import HitCountMixin
    from hitcount.settings import MODEL_HITCOUNT

    # here is an example model with a GenericRelation
    class MyModel(models.Model, HitCountMixin):

      # adding a generic relationship makes sorting by Hits possible:
      # MyModel.objects.order_by("hit_count_generic__hits")
      hit_count_generic = GenericRelation(
        MODEL_HITCOUNT, object_id_field='object_pk',
        related_query_name='hit_count_generic_relation')

    # you would access your hit_count like so:
    my_model = MyModel.objects.get(pk=1)
    my_model.hit_count.hits                 # total number of hits
    my_model.hit_count.hits_in_last(days=7) # number of hits in last seven days

Customization
-------------

`django-hitcount` allows you to customize ``HitCount`` model.

1. Define your own `hitcount` model inherited from `HitCountBase`.

2. Now when `models.py` in your application has the definition of a custom hitcount model, you need
   to instruct Django to use it for your project instead of a built-in one::

    # Somewhere in your settings.py do the following.
    # Here `myapp` is the name of your application, `MyHitCount` is the names of your customized model.

    HITCOUNT_HITCOUNT_MODEL = 'myapp.MyHitCount'


3. Run `manage.py syncdb` to install your customized models into DB.
