# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hitcount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hit',
            name='ip',
            field=models.CharField(max_length=40, db_index=True, editable=False),
        ),
        migrations.AlterField(
            model_name='hit',
            name='session',
            field=models.CharField(max_length=40, db_index=True, editable=False),
        ),
        migrations.AlterField(
            model_name='hitcount',
            name='object_pk',
            field=models.PositiveIntegerField(verbose_name='object ID'),
        ),
    ]
