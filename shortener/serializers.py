from rest_framework.serializers import ModelSerializer

from .models import ShortenedURL


class URLShortenerSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ('url',)


class URLStatisticsSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ('visitor_count', 'created_time', "url")
        read_only_fields = fields