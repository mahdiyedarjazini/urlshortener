from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_303_SEE_OTHER, HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .models import ShortenedURL
from .serializers import URLShortenerSerializer, URLStatisticsSerializer


class ShortenUrlAPIView(APIView):
    """
    API view for creating a shortened URL.

    This view handles POST requests and creates a new shortened URL.
    If the URL already exists, it returns the existing shortened URL.

    Attributes:
        post(request): Method to handle POST requests. It takes in a request,
                       validates the data, checks if the URL already exists,
                       and either returns the existing shortened URL or creates a new one.
    """
    def post(self, request):
        """
        Handle POST requests for the ShortenUrlAPIView.

        Args:
            request (Request): The request object containing the data for the URL to be shortened.

        Returns:
            Response: A response object containing the location of the shortened URL.
                      If the URL already exists, it returns a 303 status code and the location of the existing shortened URL.
                      If the URL does not exist, it creates a new shortened URL, returns a 201 status code and the location of the new shortened URL.
        """
        serializer = URLShortenerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            existing_shortened_url = ShortenedURL.get_existing_url(serializer.validated_data.get('url'))
            if existing_shortened_url:
                return Response({'location': reverse('get_original_url', args=(existing_shortened_url.slug,))},
                                HTTP_303_SEE_OTHER)
            serializer.save()
            return Response({'location': reverse('get_original_url', args=(serializer.instance.slug,))},
                            HTTP_201_CREATED)


class RetrieveShortenUrlAPIView(APIView):
    """
    API view for retrieving a shortened URL and updating its visitor count.

    This view handles GET requests and returns the details of a shortened URL.
    The short_code parameter in the GET request is used to identify the specific URL.
    It also increments the visitor count of the URL each time it is retrieved.

    Attributes:
        get(request, short_code): Method to handle GET requests. It takes in a request and a short_code,
                                   retrieves the ShortenedURL object associated with the short_code,
                                   increments its visitor count, serializes it into a response, and returns the response.
                                   If the ShortenedURL object does not exist, it returns a 404 error.
    """
    def get(self, request, short_code):
        """
        Handle GET requests for the RetrieveShortenUrlAPIView.

        Args:
            request (Request): The request object.
            short_code (str): The short code associated with the ShortenedURL object.

        Returns:
            Response: A response object containing the serialized data of the ShortenedURL object if it exists.
                      If the ShortenedURL object does not exist, it returns a 404 error.
        """
        try:
            obj = ShortenedURL.objects.get(slug=short_code)
            ShortenedURL.objects.filter(slug=short_code).update(visitor_count=obj.visitor_count + 1)
        except ObjectDoesNotExist:
            return Response({'error': 'Short url id does not exist.'}, HTTP_404_NOT_FOUND)

        serializer = URLShortenerSerializer(obj)
        return Response(serializer.data, HTTP_200_OK)


class ShortenedUrlStatisticsAPIView(APIView):
    """
    API view for retrieving statistics of a shortened URL.

    This view handles GET requests and returns the statistics of a shortened URL.
    The short_code parameter in the GET request is used to identify the specific URL.

    Attributes:
        get(request, short_code): Method to handle GET requests. It takes in a request and a short_code,
                                   retrieves the ShortenedURL object associated with the short_code,
                                   serializes it into a response, and returns the response.
                                   If the ShortenedURL object does not exist, it returns a 404 error.
    """
    def get(self, request, short_code):
        """
        Handle GET requests for the ShortenedUrlStatisticsAPIView.

        Args:
            request (Request): The request object.
            short_code (str): The short code associated with the ShortenedURL object.

        Returns:
            Response: A response object containing the serialized data of the ShortenedURL object if it exists.
                      If the ShortenedURL object does not exist, it returns a 404 error.
        """
        try:
            obj = ShortenedURL.objects.get(slug=short_code)
        except ObjectDoesNotExist:
            return Response({'error': 'Short url id does not exist.'}, HTTP_404_NOT_FOUND)

        serializer = URLStatisticsSerializer(obj)
        return Response(serializer.data, HTTP_200_OK)
