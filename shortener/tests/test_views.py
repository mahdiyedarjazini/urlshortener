import pytest
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework.test import APIClient

from shortener.serializers import URLShortenerSerializer

pytestmark = pytest.mark.django_db


class TestShortenUrlAPIView:
    def test_create_shortened_url(self):
        client = APIClient()
        url = '/urls/shorten/'
        data = {
            "url": "https://some.long.url.test/foo/bar",
        }
        response = client.post(url, data, format='json')
        assert response.status_code == HTTP_201_CREATED
        assert 'location' in response.data


class TestRetrieveShortenUrlAPIView:
    @pytest.fixture
    def slug(self):
        serializer = URLShortenerSerializer(data={'url': 'https://some.long.url.test/foo/bar'})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.instance.slug

    def test_get_original_url(self, slug):
        client = APIClient()
        url = f'/urls/{slug}/'
        response = client.get(url, format='json')
        assert response.status_code == HTTP_200_OK
        assert 'https://some.long.url.test/foo/bar' == response.data['location']


class TestShortenedUrlStatisticsAPIView:
    @pytest.fixture
    def slug(self):
        serializer = URLShortenerSerializer(data={'url': 'https://some.long.url.test/foo/bar'})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.instance.slug

    def test_get_stats(self, slug):
        client = APIClient()
        get_url = f'/urls/{slug}/'
        stats_url = f'/urls/{slug}/stats/'
        client.get(get_url, format='json')
        client.get(get_url, format='json')
        client.get(get_url, format='json')
        response = client.get(stats_url, format='json')
        assert response.status_code == HTTP_200_OK
        assert 3 == response.data['visitor_count']
