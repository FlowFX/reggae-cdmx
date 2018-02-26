"""Models for calendar app."""
import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


app_name = 'events'


class Event(models.Model):
    """The event model. The main model in this project."""

    slug = models.SlugField(max_length=255)
    title = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)
    venue = models.ForeignKey(
        'venues.Venue',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='events',
    )
    description = models.TextField(verbose_name='', blank=True)
    fb_event_url = models.URLField(verbose_name='URL of the corresponding Facebook event', blank=True)
    flyer_image = models.ImageField(
        upload_to='event_flyers',
        verbose_name='image file of the event\'s promotion flyer',
        blank=True,
    )

    def __str__(self):
        """Return string representation of event.

        event_title - event_date
        """
        return '{0} - {1}'.format(self.title, self.date)

    def generate_slug(self):
        """Return a unique slug generated from the event's date and title."""
        date = str(self.date)
        title = self.title

        return slugify(f'{date} {title}')

    def get_absolute_url(self):
        """Return the event's detail page URL."""
        return reverse('events:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """Override default save method."""
        self.slug = self.generate_slug()

        super(Event, self).save(*args, **kwargs)
