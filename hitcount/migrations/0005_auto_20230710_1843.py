# Generated by Django 3.1.14 on 2023-07-10 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hitcount', '0004_auto_20200704_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blacklistip',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='blacklistuseragent',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hit',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='hitcount',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
