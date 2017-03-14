"""Reggae CDMX URL Configuration."""

from django.conf import settings
from django.conf.urls import include, url

from reggae_cdmx import views


urlpatterns = [
    # Events
    url(r'^$', views.EventListView.as_view(), name='index'),
    url(r'^new$', views.EventCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/edit$', views.EventUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', views.EventDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>[0-9]+)/$', views.EventDetailView.as_view(), name='detail'),
    # Venues
    url(r'^venues/$', views.VenueListView.as_view(), name='venue_list'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
