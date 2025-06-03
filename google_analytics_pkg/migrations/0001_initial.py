# analytics/migrations/0001_initial.py

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='GAConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_id', models.CharField(max_length=50)),
                ('measurement_id', models.CharField(max_length=50)),
                ('api_secret', models.CharField(max_length=100)),
                ('credentials_json', models.TextField()),
            ],
        ),
    ]
