"""Models for calendar app."""

from django.db import models

from django.urls import reverse

import datetime


class Venue(models.Model):

    name = models.CharField(max_length=255)


class Event(models.Model):
    """The event model. The main model in this project."""

    title = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    venue = models.ForeignKey(
        'Venue',
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        """Return the event's detail page URL."""
        return reverse('detail', args=[str(self.id)])
