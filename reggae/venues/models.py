"""Model definitions for the venues app."""
from django.db import models


class Venue(models.Model):
    """The venue model."""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Return string representation of Venue instance.

        venue.name
        """
        return '{0}'.format(self.name)
