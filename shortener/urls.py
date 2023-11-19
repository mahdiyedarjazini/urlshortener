from django.urls import path

from .views import ShortenUrlAPIView, RetrieveShortenUrlAPIView, ShortenedUrlStatisticsAPIView

urlpatterns = [
    path('shorten/', ShortenUrlAPIView.as_view(), name='create_short_url'),
    path('<short_code>/', RetrieveShortenUrlAPIView.as_view(), name='get_original_url'),
    path('<short_code>/stats/', ShortenedUrlStatisticsAPIView.as_view(), name='get_shortened_url_statistics'),
]
