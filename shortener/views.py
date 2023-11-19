from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_303_SEE_OTHER, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .models import ShortenedURL
from .serializers import URLShortenerSerializer, URLStatisticsSerializer


class ShortenUrlAPIView(APIView):
    def post(self, request):
        serializer = URLShortenerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            existing_shortened_url = ShortenedURL.get_existing_url(serializer.validated_data.get('url'))
            if existing_shortened_url:
                return Response({'location': reverse('get_original_url', args=(existing_shortened_url.slug,))},
                                HTTP_303_SEE_OTHER)
            serializer.save()
            return Response({'location': reverse('get_original_url', args=(serializer.instance.slug,))}, HTTP_201_CREATED)


class RetrieveShortenUrlAPIView(APIView):
    def get(self, request, short_code):
        try:
            obj = ShortenedURL.objects.get(slug=short_code)
            ShortenedURL.objects.filter(slug=short_code).update(visitor_count=obj.visitor_count + 1)
        except ObjectDoesNotExist:
            return Response({'error': 'Short url id does not exist.'}, HTTP_404_NOT_FOUND)

        serializer = URLShortenerSerializer(obj)
        return Response(serializer.data, HTTP_200_OK)


class ShortenedUrlStatisticsAPIView(APIView):
    def get(self, request, short_code):
        try:
            obj = ShortenedURL.objects.get(slug=short_code)
        except ObjectDoesNotExist:
            return Response({'error': 'Short url id does not exist.'}, HTTP_404_NOT_FOUND)

        serializer = URLStatisticsSerializer(obj)
        return Response(serializer.data, HTTP_200_OK)