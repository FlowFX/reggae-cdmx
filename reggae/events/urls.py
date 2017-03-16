"""Events URLs."""

from django.conf.urls import url

from .views import (EventCreateView, EventDeleteView, EventDetailView,
                    EventListView, EventUpdateView)


urlpatterns = [
    url(r'^$', EventListView.as_view(), name='list'),
    url(r'^new$', EventCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[0-9]+)/edit$', EventUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>[0-9]+)/delete$', EventDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>[0-9]+)/$', EventDetailView.as_view(), name='detail'),
]







