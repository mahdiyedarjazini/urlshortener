from rest_framework.serializers import ModelSerializer

from .models import ShortenedURL


class URLShortenerSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['url', 'slug']
        readonly_fields = ['slug']


class URLStatisticsSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        readonly_fields = ['visitor_count']
