# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(unique=True, max_length=40)),
            ],
            options={
                'db_table': 'hitcount_blacklist_ip',
                'verbose_name': 'Blacklisted IP',
                'verbose_name_plural': 'Blacklisted IPs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlacklistUserAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_agent', models.CharField(unique=True, max_length=255)),
            ],
            options={
                'db_table': 'hitcount_blacklist_user_agent',
                'verbose_name': 'Blacklisted User Agent',
                'verbose_name_plural': 'Blacklisted User Agents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ip', models.CharField(max_length=40, editable=False)),
                ('session', models.CharField(max_length=40, editable=False)),
                ('user_agent', models.CharField(max_length=255, editable=False)),
            ],
            options={
                'ordering': ('-created',),
                'get_latest_by': 'created',
                'verbose_name': 'hit',
                'verbose_name_plural': 'hits',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HitCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_pk', models.PositiveIntegerField(verbose_name='object ID')),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_hitcount',
                                                   to='contenttypes.ContentType', on_delete=models.CASCADE)),
            ],
            options={
                'get_latest_by': 'modified',
                'ordering': ('-hits',),
                'verbose_name_plural': 'hit counts',
                'db_table': 'hitcount_hit_count',
                'verbose_name': 'hit count',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='hitcount',
            unique_together=set([('content_type', 'object_pk')]),
        ),
        migrations.AddField(
            model_name='hit',
            name='hitcount',
            field=models.ForeignKey(editable=False, to='hitcount.HitCount', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hit',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
