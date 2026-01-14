from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_analytics_pkg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gaconfiguration',
            name='search_console_html_tag',
            field=models.TextField(null=True, blank=True),
        ),
    ]
