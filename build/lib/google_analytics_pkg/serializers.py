# serializers.py
from rest_framework import serializers
from .models import GAConfiguration, GAEventLog

class GAConfigurationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False) 
    class Meta:
        model = GAConfiguration
        fields = ['id','property_id', 'measurement_id', 'api_secret', 'credentials_json', 'search_console_html_tag']
class GAEventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GAEventLog
        fields = ['event_name', 'params', 'timestamp']
# class GAReportCacheSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GoogleAnalytics.GAReportCache
#         fields = ['metric', 'dimension', 'value', 'retrieved_at']
        
class GAEventSerializer(serializers.Serializer):
    event_name = serializers.CharField(max_length=100)
    params = serializers.DictField(child=serializers.CharField(), required=False)
    client_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
