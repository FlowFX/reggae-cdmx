"""Models for calendar app."""

from django.db import models

from django.urls import reverse

import datetime


class Event(models.Model):

    title = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])
