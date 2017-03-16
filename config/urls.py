"""Reggae CDMX URL Configuration."""

from django.conf import settings
from django.conf.urls import include, url

from reggae.events.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    # Events
    url(r'^events/', include('reggae.events.urls', namespace='events')),
    url(r'^venues/', include('reggae.venues.urls', namespace='venues')),
    # Venues
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
