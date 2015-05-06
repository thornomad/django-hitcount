# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(editable=False)),
                ('ip', models.CharField(max_length=40, editable=False)),
                ('session', models.CharField(max_length=40, editable=False)),
                ('user_agent', models.CharField(max_length=255, editable=False)),
            ],
            options={
                'ordering': ('-created',),
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='HitCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('modified', models.DateTimeField(default=datetime.datetime.utcnow)),
                ('object_pk', models.TextField(verbose_name=b'object ID')),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_hitcount', verbose_name=b'content type', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-hits',),
                'db_table': 'hitcount_hit_count',
                'verbose_name': 'Hit Count',
                'verbose_name_plural': 'Hit Counts',
                'get_latest_by': 'modified',
            },
        ),
        migrations.AddField(
            model_name='hit',
            name='hitcount',
            field=models.ForeignKey(editable=False, to='hitcount.HitCount'),
        ),
        migrations.AddField(
            model_name='hit',
            name='user',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
