# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.db.models import F
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from etc.toolbox import get_model_class_from_string

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

from .managers import HitCountManager, HitManager
from .settings import MODEL_HITCOUNT
from .signals import delete_hit_count


@receiver(delete_hit_count)
def delete_hit_count_handler(sender, instance, save_hitcount=False, **kwargs):
    """
    Custom callback for the Hit.delete() method.

    Hit.delete(): removes the hit from the associated HitCount object.
    Hit.delete(save_hitcount=True): preserves the hit for the associated
    HitCount object.

    """
    if not save_hitcount:
        instance.hitcount.decrease()


class HitCountBase(models.Model):
    """
    Base class for hitcount models.

    Model that stores the hit totals for any content object.

    """
    hits = models.PositiveIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(
        ContentType, related_name="content_type_set_for_%(class)s", on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField(verbose_name='object ID')
    content_object = GenericForeignKey('content_type', 'object_pk')

    objects = HitCountManager()

    class Meta:
        abstract = True
        ordering = ('-hits',)
        get_latest_by = "modified"
        verbose_name = _("hit count")
        verbose_name_plural = _("hit counts")
        unique_together = ("content_type", "object_pk")

    def __str__(self):
        return '%s' % self.content_object

    def increase(self):
        self.hits = F('hits') + 1
        self.save()

    def decrease(self):
        self.hits = F('hits') - 1
        self.save()

    def hits_in_last(self, **kwargs):
        """
        Returns hit count for an object during a given time period.

        This will only work for as long as hits are saved in the Hit database.
        If you are purging your database after 45 days, for example, that means
        that asking for hits in the last 60 days will return an incorrect
        number as that the longest period it can search will be 45 days.

        For example: hits_in_last(days=7).

        Accepts days, seconds, microseconds, milliseconds, minutes,
        hours, and weeks.  It's creating a datetime.timedelta object.

        """
        assert kwargs, "Must provide at least one timedelta arg (eg, days=1)"

        period = timezone.now() - timedelta(**kwargs)
        return self.hit_set.filter(created__gte=period).count()

    # def get_content_object_url(self):
    #     """
    #     Django has this in its contrib.comments.model file -- seems worth
    #     implementing though it may take a couple steps.
    #
    #     """
    #     pass


class HitCount(HitCountBase):
    """Built-in hitcount class. Default functionality."""

    class Meta(HitCountBase.Meta):
        db_table = "hitcount_hit_count"


class Hit(models.Model):
    """
    Model captures a single Hit by a visitor.

    None of the fields are editable because they are all dynamically created.
    Browsing the Hit list in the Admin will allow one to blacklist both
    IP addresses as well as User Agents. Blacklisting simply causes those
    hits to not be counted or recorded.

    Depending on how long you set the HITCOUNT_KEEP_HIT_ACTIVE, and how long
    you want to be able to use `HitCount.hits_in_last(days=30)` you can choose
    to clean up your Hit table by using the management `hitcount_cleanup`
    management command.

    """
    created = models.DateTimeField(editable=False, auto_now_add=True, db_index=True)
    ip = models.CharField(max_length=40, editable=False, db_index=True)
    session = models.CharField(max_length=40, editable=False, db_index=True)
    user_agent = models.CharField(max_length=255, editable=False)
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, editable=False, on_delete=models.CASCADE)
    hitcount = models.ForeignKey(MODEL_HITCOUNT, editable=False, on_delete=models.CASCADE)

    objects = HitManager()

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'
        verbose_name = _("hit")
        verbose_name_plural = _("hits")

    def __str__(self):
        return 'Hit: %s' % self.pk

    def save(self, *args, **kwargs):
        """
        The first time the object is created and saved, we increment
        the associated HitCount object by one. The opposite applies
        if the Hit is deleted.

        """
        if self.pk is None:
            self.hitcount.increase()

        super(Hit, self).save(*args, **kwargs)

    def delete(self, save_hitcount=False):
        """
        If a Hit is deleted and save_hitcount=True, it will preserve the
        HitCount object's total. However, under normal circumstances, a
        delete() will trigger a subtraction from the HitCount object's total.

        NOTE: This doesn't work at all during a queryset.delete().

        """
        delete_hit_count.send(
            sender=self, instance=self, save_hitcount=save_hitcount)
        super(Hit, self).delete()


class BlacklistIP(models.Model):

    ip = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = "hitcount_blacklist_ip"
        verbose_name = _("Blacklisted IP")
        verbose_name_plural = _("Blacklisted IPs")

    def __str__(self):
        return '%s' % self.ip


class BlacklistUserAgent(models.Model):

    user_agent = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "hitcount_blacklist_user_agent"
        verbose_name = _("Blacklisted User Agent")
        verbose_name_plural = _("Blacklisted User Agents")

    def __str__(self):
        return '%s' % self.user_agent


class HitCountMixin(object):
    """
    HitCountMixin provides an easy way to add a `hit_count` property to your
    model that will return the related HitCount object.
    """

    @property
    def hit_count(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        hit_count, created = get_model_class_from_string(MODEL_HITCOUNT).objects.get_or_create(
            content_type=ctype, object_pk=self.pk)
        return hit_count
