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
    if not save_hitcount:
        instance.hitcount.decrease()


class HitCountBase(models.Model):
    hits = models.PositiveIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, related_name=
        'content_type_set_for_%(class)s', on_delete=models.CASCADE)
    object_pk = models.PositiveIntegerField(verbose_name='object ID')
    content_object = GenericForeignKey('content_type', 'object_pk')
    objects = HitCountManager()


    class Meta:
        abstract = True
        ordering = '-hits',
        get_latest_by = 'modified'
        verbose_name = _('hit count')
        verbose_name_plural = _('hit counts')
        unique_together = 'content_type', 'object_pk'

    def __str__(self):
        return '%s' % self.content_object

    def increase(self):
        self.hits = F('hits') + 1
        self.save()

    def decrease(self):
        self.hits = F('hits') - 1
        self.save()

    def hits_in_last(self, **kwargs):
        assert kwargs, 'Must provide at least one timedelta arg (eg, days=1)'
        period = timezone.now() - timedelta(**kwargs)
        return self.hit_set.filter(created__gte=period).count()


class HitCount(HitCountBase):


    class Meta(HitCountBase.Meta):
        db_table = 'hitcount_hit_count'


class Hit(models.Model):
    created = models.DateTimeField(editable=False, auto_now_add=True,
        db_index=True)
    ip = models.CharField(max_length=40, editable=False, db_index=True)
    session = models.CharField(max_length=40, editable=False, db_index=True)
    user_agent = models.CharField(max_length=255, editable=False)
    domain = models.CharField(max_length=255, editable=False, default='')
    user = models.ForeignKey(AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.CASCADE)
    hitcount = models.ForeignKey(MODEL_HITCOUNT, editable=False, on_delete=
        models.CASCADE)
    objects = HitManager()


    class Meta:
        ordering = '-created',
        get_latest_by = 'created'
        verbose_name = _('hit')
        verbose_name_plural = _('hits')

    def __str__(self):
        return 'Hit: %s' % self.pk

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.hitcount.increase()
        super(Hit, self).save(*args, **kwargs)

    def delete(self, save_hitcount=False):
        delete_hit_count.send(sender=self, instance=self, save_hitcount=
            save_hitcount)
        super(Hit, self).delete()


class BlacklistIP(models.Model):
    ip = models.CharField(max_length=40, unique=True)


    class Meta:
        db_table = 'hitcount_blacklist_ip'
        verbose_name = _('Blacklisted IP')
        verbose_name_plural = _('Blacklisted IPs')

    def __str__(self):
        return '%s' % self.ip


class BlacklistUserAgent(models.Model):
    user_agent = models.CharField(max_length=255, unique=True)


    class Meta:
        db_table = 'hitcount_blacklist_user_agent'
        verbose_name = _('Blacklisted User Agent')
        verbose_name_plural = _('Blacklisted User Agents')

    def __str__(self):
        return '%s' % self.user_agent


class HitCountMixin(object):

    @property
    def hit_count(self):
        ctype = ContentType.objects.get_for_model(self.__class__)
        hit_count, created = get_model_class_from_string(MODEL_HITCOUNT
            ).objects.get_or_create(content_type=ctype, object_pk=self.pk)
        return hit_count
