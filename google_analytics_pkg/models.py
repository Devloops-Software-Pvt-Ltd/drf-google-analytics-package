from django.db import models


class GAConfiguration(models.Model):
    property_id = models.CharField(max_length=50)
    measurement_id = models.CharField(max_length=50)
    api_secret = models.CharField(max_length=100)
    credentials_json = models.TextField()  # Encrypted in real case
    search_console_html_tag = models.TextField(null=True, blank=True)
    
class GAEventLog(models.Model):

    event_name = models.CharField(max_length=100)
    params = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)

# class GAReportCache(models.Model):
#     metric = models.CharField(max_length=100)
#     dimension = models.CharField(max_length=100, null=True, blank=True)
#     value = models.FloatField()
#     retrieved_at = models.DateTimeField(auto_now=True)
