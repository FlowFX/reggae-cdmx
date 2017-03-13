"""Views for calendar app."""

from .models import Event

from django.views.generic import DetailView, ListView



class EventDetailView(DetailView):
    template_name = 'event_detail.html'
    model = Event
    context_object_name = 'event'


class EventListView(ListView):
    template_name = 'index.html'
    model = Event
    context_object_name = 'events'
