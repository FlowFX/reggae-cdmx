"""ModelAdmins for the events app."""
from app.events.models import Event

from django.contrib import admin


class EventAdmin(admin.ModelAdmin):  # noqa: D101
    list_display = ('date', 'title', 'venue')
    ordering = ['-date']


admin.site.register(Event, EventAdmin)
