"""Models for calendar app."""

from django.db import models
from django.urls import reverse

import datetime


class Event(models.Model):
    """The event model. The main model in this project."""

    title = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    venue = models.ForeignKey(
        'venues.Venue',
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        """Return the event's detail page URL."""
        return reverse('events:detail', args=[str(self.id)])

    def __str__(self):
        """Return string representation of event.

        event_title - event_date
        """
        return '{0} - {1}'.format(self.title, self.date)
