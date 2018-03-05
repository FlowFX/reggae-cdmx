"""Models for calendar app."""
import datetime

from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
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
    description = models.TextField(blank=True)
    fb_event_url = models.URLField(blank=True)
    flyer_image = models.ImageField(
        upload_to='event_flyers',
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
        """Override default save method.

        Create new slug if necessary.
        Create new redirect if slug/URL changes.

        The slug changes when the date or title of the event changes. We want to always use the current
        slug/URL, but don't invalidate the old URLs.
        """
        try:
            old_url = self.get_absolute_url()
        except NoReverseMatch:
            old_url = None

        self.slug = self.generate_slug()
        new_url = self.get_absolute_url()

        if old_url and old_url != new_url:
            site = Site.objects.get_current()
            Redirect(old_path=old_url, new_path=new_url, site=site).save()

        super(Event, self).save(*args, **kwargs)
