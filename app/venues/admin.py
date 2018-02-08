"""ModelAdmins for the venues app."""
from app.venues.models import Venue

from django.contrib import admin


class VenueAdmin(admin.ModelAdmin):  # noqa: D101
    pass


admin.site.register(Venue, VenueAdmin)
