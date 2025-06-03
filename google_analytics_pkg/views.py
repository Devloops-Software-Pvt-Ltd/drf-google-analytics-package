from rest_framework import generics, status
from rest_framework.response import Response
from .models import GAConfiguration
import uuid
import requests
from .serializers import GAConfigurationSerializer
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

import json
class GAConfigurationViewSet(viewsets.ModelViewSet):
    queryset = GAConfiguration.objects.all()
    serializer_class = GAConfigurationSerializer

    def create(self, request, *args, **kwargs):
        if GAConfiguration.objects.exists():
            raise ValidationError({"detail": "GAConfiguration already exists. Please update the existing configuration."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def list(self, request):
        ga_config = self.queryset
        serializer = self.serializer_class(ga_config, many=True)
        return Response({
            "code": "0", 
            "message": "GA  configurations retrieved successfully.", 
            "data": serializer.data
        })
class GAEventAPIView(generics.GenericAPIView):
    def post(self, request):
        event_name = request.data.get("event_name")
        params = request.data.get("params", {})
        client_id = request.data.get("client_id")

        if not event_name:
            return Response({"error": "event_name is required"}, status=400)

        try:
            config = GAConfiguration.objects.first()
            if not config:
                return Response({"error": "GAConfiguration not found"}, status=500)
        except Exception as e:
            return Response({"error": f"Failed to load GA configuration: {str(e)}"}, status=500)

        try:
            success = send_ga_event(config, event_name, params, client_id)
            if success:
                return Response({"success": True})
            else:
                return Response({"success": False}, status=500)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
        except requests.HTTPError as he:
            return Response({"error": str(he)}, status=502)
        
    



def send_ga_event(config, event_name, params, client_id=None):
    client_id = client_id or str(uuid.uuid4())

    # Make sure params is a dict
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except json.JSONDecodeError:
            raise ValueError("params is a string but not valid JSON")

    if not isinstance(params, dict):
        raise ValueError("params must be a dict")



    url = (
        "https://www.google-analytics.com/debug/mp/collect"
        f"?measurement_id={config.measurement_id}"
        f"&api_secret={config.api_secret}"
    )

    payload = {
        "client_id": client_id,
        "events": [{
            "name": event_name,
            "params": params
        }],
        "user_properties": {
            "debug_mode": {"value": "true"}
        }
    }

    response = requests.post(url, json=payload)
    print("Status:", response.status_code)
    print("Response:", response.text)

    response.raise_for_status()  # Raise HTTPError on bad status

    # # Optionally check validation messages
    # response_data = response.json()
    # if "validationMessages" in response_data:
    #     print("GA Validation messages:", response_data["validationMessages"])

    return response.status_code == 200
