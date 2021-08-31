from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('hitcount', '0004_auto_20200704_0933')]
    operations = [migrations.AddField(model_name='hit', name='domain',
        field=models.CharField(default=None, editable=False, max_length=255
        ), preserve_default=False)]
