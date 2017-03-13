"""Models for calendar app."""

from django.db import models

from django.urls import reverse


class Event(models.Model):

    title = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])
