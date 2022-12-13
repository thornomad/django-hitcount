# Generated by Django 4.1.2 on 2022-11-30 12:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistIP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=40, unique=True)),
            ],
            options={
                'verbose_name': 'Blacklisted IP',
                'verbose_name_plural': 'Blacklisted IPs',
                'db_table': 'hitcount_blacklist_ip',
            },
        ),
        migrations.CreateModel(
            name='BlacklistUserAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agent', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Blacklisted User Agent',
                'verbose_name_plural': 'Blacklisted User Agents',
                'db_table': 'hitcount_blacklist_user_agent',
            },
        ),
        migrations.CreateModel(
            name='HitCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hits', models.PositiveIntegerField(default=0)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('object_pk', models.PositiveIntegerField(verbose_name='object ID')),
                ('domain', models.CharField(default='', editable=False, max_length=255)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_type_set_for_%(class)s', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'hit count',
                'verbose_name_plural': 'hit counts',
                'db_table': 'hitcount_hit_count',
                'ordering': ('-hits',),
                'get_latest_by': 'modified',
                'abstract': False,
                'unique_together': {('content_type', 'object_pk')},
            },
        ),
        migrations.CreateModel(
            name='Hit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('ip', models.CharField(db_index=True, editable=False, max_length=40)),
                ('session', models.CharField(db_index=True, editable=False, max_length=40)),
                ('user_agent', models.CharField(editable=False, max_length=255)),
                ('domain', models.CharField(default='', editable=False, max_length=255)),
                ('hitcount', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='hitcount.hitcount')),
                ('user', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'hit',
                'verbose_name_plural': 'hits',
                'ordering': ('-created',),
                'get_latest_by': 'created',
            },
        ),
    ]
