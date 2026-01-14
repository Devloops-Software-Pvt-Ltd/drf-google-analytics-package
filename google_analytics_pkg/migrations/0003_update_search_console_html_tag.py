from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_analytics_pkg', '0002_add_search_console_html_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gaconfiguration',
            name='search_console_html_tag',
            field=models.TextField(null=True, blank=True),
        ),
    ]
