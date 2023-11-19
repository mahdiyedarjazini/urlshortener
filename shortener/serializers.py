from rest_framework.serializers import ModelSerializer

from .models import ShortenedURL


class URLShortenerSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ('url',)


class URLStatisticsSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        read_only_fields = ['visitor_count']
