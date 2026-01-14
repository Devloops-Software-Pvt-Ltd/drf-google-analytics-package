from django.db import models


class GAConfiguration(models.Model):
    property_id = models.CharField(max_length=50)
    measurement_id = models.CharField(max_length=50)
    api_secret = models.CharField(max_length=100)
    credentials_json = models.TextField()  # Encrypted in real case

    # HTML verification tag for Google Search Console (optional)
    search_console_html_tag = models.TextField(null=True, blank=True)

class GAEventLog(models.Model):

    event_name = models.CharField(max_length=100)
    params = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
