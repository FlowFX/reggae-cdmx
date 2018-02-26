"""Events URLs."""
from django.urls import path

from .views import (EventCreateView, EventDeleteView, EventDetailView,
                    EventListView, EventUpdateView)


app_name = 'events'


urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('new', EventCreateView.as_view(), name='create'),
    path('<str:slug>/edit', EventUpdateView.as_view(), name='update'),
    path('<str:slug>/delete', EventDeleteView.as_view(), name='delete'),
    path('<str:slug>/', EventDetailView.as_view(), name='detail'),
]
