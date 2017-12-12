"""Events URLs."""
from django.urls import path

from .views import (EventCreateView, EventDeleteView, EventDetailView,
                    EventListView, EventUpdateView)


app_name = 'events'


urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('new', EventCreateView.as_view(), name='create'),
    path('<int:pk>/edit', EventUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', EventDeleteView.as_view(), name='delete'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail'),
]
