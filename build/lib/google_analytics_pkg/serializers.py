# serializers.py
import re
from rest_framework import serializers
from .models import GAConfiguration, GAEventLog

_META_NAME_RE = re.compile(r'<meta[^>]+name\s*=\s*["\']google-site-verification["\'][^>]*>', re.IGNORECASE)
_CONTENT_ATTR_RE = re.compile(r'content\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
_TOKEN_RE = re.compile(r'^[A-Za-z0-9_\-]{10,}$')


class GAConfigurationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    search_console_html_tag = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = GAConfiguration
        fields = ['id','property_id', 'measurement_id', 'api_secret', 'credentials_json', 'search_console_html_tag']

    def validate_search_console_html_tag(self, value):
        if value in (None, ''):
            return value

        val = value.strip()
        if _META_NAME_RE.search(val):
            m = _CONTENT_ATTR_RE.search(val)
            if not m:
                raise serializers.ValidationError(
                    "Meta tag must include a content attribute with the verification token."
                )
            token = m.group(1).strip()
            if not _TOKEN_RE.match(token):
                raise serializers.ValidationError(
                    "Verification token in the content attribute looks invalid."
                )
            return val

        if _TOKEN_RE.match(val):
            return val

        raise serializers.ValidationError(
            'Provide either a valid Search Console meta tag containing '
            'name="google-site-verification" or the raw verification token.'
        )


class GAEventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GAEventLog
        fields = ['event_name', 'params', 'timestamp']
        
class GAEventSerializer(serializers.Serializer):
    event_name = serializers.CharField(max_length=100)
    params = serializers.DictField(child=serializers.CharField(), required=False)
    client_id = serializers.CharField(max_length=50, required=False, allow_blank=True)
