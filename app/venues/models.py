"""Model definitions for the venues app."""
from django.db import models


app_name = 'venues'


class Venue(models.Model):
    """The venue model."""

    name = models.CharField('nombre', max_length=255)
    address = models.CharField('dirección', max_length=1024, blank=True)
    url = models.URLField('URL', blank=True)

    def __str__(self):
        """Return string representation of Venue instance.

        venue.name
        """
        return '{0}'.format(self.name)
