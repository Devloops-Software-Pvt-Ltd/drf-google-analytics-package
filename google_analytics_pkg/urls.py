from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GAConfigurationViewSet,GAEventAPIView

router = DefaultRouter()
router.register(r'google-analytics', GAConfigurationViewSet, basename='google-analytics')

urlpatterns = [
    path('', include(router.urls)),

    path('google-analytics-event/',GAEventAPIView.as_view(), name='google-analytics-event'),
]
