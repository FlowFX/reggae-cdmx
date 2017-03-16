
from django.conf.urls import url

from .views import (VenueCreateView, VenueDeleteView, VenueDetailView,
                    VenueListView, VenueUpdateView)


urlpatterns = [
    url(r'^$', VenueListView.as_view(), name='list'),
    url(r'^new$', VenueCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/$', VenueDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit$', VenueUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', VenueDeleteView.as_view(), name='delete'),
]



