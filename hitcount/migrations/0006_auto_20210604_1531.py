from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('hitcount', '0005_hit_domain')]
    operations = [migrations.AlterField(model_name='hit', name='domain',
        field=models.CharField(default='', editable=False, max_length=255))]
