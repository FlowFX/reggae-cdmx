"""URL definitions for the venues app."""
from django.urls import path

from .views import (VenueCreateView, VenueDeleteView, VenueDetailView,
                    VenueListView, VenueUpdateView)


app_name = 'venues'


urlpatterns = [
    path('', VenueListView.as_view(), name='list'),
    path('new', VenueCreateView.as_view(), name='create'),
    path('<int:pk>/', VenueDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', VenueUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', VenueDeleteView.as_view(), name='delete'),
]
