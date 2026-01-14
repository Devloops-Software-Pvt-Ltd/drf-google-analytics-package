# serializers.py
import re
from rest_framework import serializers
from .models import GAConfiguration, GAEventLog

# Regexes used for validation
_META_NAME_RE = re.compile(r'<meta[^>]+name\s*=\s*["\']google-site-verification["\'][^>]*>', re.IGNORECASE)
_CONTENT_ATTR_RE = re.compile(r'content\s*=\s*["\']([^"\']+)["\']', re.IGNORECASE)
_TOKEN_RE = re.compile(r'^[A-Za-z0-9_\-]{10,}$')  # token-like string (adjust min length if needed)


class GAConfigurationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    # explicit field to allow blank/null and to attach validation method
    search_console_html_tag = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )

    class Meta:
        model = GAConfiguration
        fields = [
            'id',
            'property_id',
            'measurement_id',
            'api_secret',
            'credentials_json',
            'search_console_html_tag',  # new field
        ]

    def validate_search_console_html_tag(self, value):
        """
        Accepts:
         - empty / None (no verification)
         - a full meta tag containing name="google-site-verification" and a content attribute
         - a raw verification token (alphanumeric with - or _)

        Returns the original value (or stripped token) or raises ValidationError.
        """
        if value in (None, ''):
            return value

        val = value.strip()

        # Case 1: full meta tag with name="google-site-verification"
        if _META_NAME_RE.search(val):
            # ensure content attribute exists and looks like a token
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

        # Case 2: raw token
        if _TOKEN_RE.match(val):
            return val

        # Otherwise invalid
        raise serializers.ValidationError(
            'Provide either a valid Search Console meta tag containing '
            'name="google-site-verification" or the raw verification token.'
        )


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
