"""Reggae CDMX URL Configuration."""

from django.conf import settings
from django.conf.urls import include, url

from app.events.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    # Events
    url(r'^events/', include('app.events.urls', namespace='events')),
    # Venues
    url(r'^venues/', include('app.venues.urls', namespace='venues')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
