from django.db import models

from django.urls import reverse


class Venue(models.Model):
    """The venue model."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return '{0}'.format(self.name)