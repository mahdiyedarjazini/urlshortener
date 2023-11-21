from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from utils.models import BaseModel


class ShortenedURL(BaseModel):
    slug = models.CharField(max_length=6, verbose_name=_('slug'), unique=True)
    url = models.URLField(verbose_name=_('url'))
    visitor_count = models.IntegerField(verbose_name=_('visitor_count'), null=True, default=0)

    @classmethod
    def validate_slug(cls, slug):
        """
        Validates a slug that can be used to identify the original URL.

        This method checks if the provided slug already exists. If it does, the method recursively generates random
        strings of length 6 until a unique slug is generated.

        :param slug: The initial slug string to be validated.
        :type slug: str
        :return: A unique slug as a string.
        :rtype: str
        """
        while cls.get_existing_slug(slug):
            slug = get_random_string(length=6)
        return slug

    @classmethod
    def get_existing_slug(cls, string):
        """
        Checks whether a given string already exists as a slug in the database.

        This method queries the database to see if the provided string already exists as a slug.
        It is used to ensure that each slug in the database is unique.

        :param string: The string to check for uniqueness. This is the potential slug that we want to insert into the database.
        :type string: str
        :return: True if the string already exists as a slug in the database, False otherwise.
        :rtype: bool
        """
        return cls.objects.filter(slug=string).exists()

    @classmethod
    def get_existing_url(cls, url):
        """
        Checks whether a given URL already exists in the database.

        This method queries the database to see if the provided URL already exists.
        It is used to ensure that each URL in the database is unique.

        :param url: The URL to check for existence in the database. This is the URL that we want to verify.
        :type url: str
        :return: The existing object in the database if the URL exists, None otherwise.
        :rtype: Django Model instance or None
        """
        try:
            return cls.objects.get(url=url)
        except ObjectDoesNotExist:
            return

    def save(self, *args, **kwargs):
        """
        Overwrites the existing save() method to automatically generate the identifier.

        This method generates a unique slug using the generate_slug() method before saving the object.
        This ensures that every saved object has a unique slug.

        :param args: Variable length argument list.
        :param kwargs: Arbitrary keyword arguments.
        :return: The result of the parent class's save() method.
        """
        slug = get_random_string(length=6)
        self.slug = self.validate_slug(slug)
        return super().save(*args, **kwargs)
