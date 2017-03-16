"""Models for calendar app."""

from django.db import models

from django.urls import reverse

import datetime


class Venue(models.Model):
    """The venue model."""

    name = models.CharField(max_length=255)

    def __str__(self):
        return '{0}'.format(self.name)


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
        return reverse('event_detail', args=[str(self.id)])

    def __str__(self):
        return '{0} - {1}'.format(self.title, self.date)