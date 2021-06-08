from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('hitcount', '0002_index_ip_and_session')]
    operations = [migrations.AlterField(model_name='hitcount', name=
        'object_pk', field=models.CharField(max_length=128, verbose_name=
        'object ID'))]
