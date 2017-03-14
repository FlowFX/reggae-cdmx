"""Views for calendar app."""
from django.urls import reverse

from .models import Event, Venue
from .forms import EventForm

from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class EventDetailView(DetailView):
    """DetailView for the Event model."""

    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


class EventCreateView(CreateView):
    """CreateView for the Event model."""

    model = Event
    form_class = EventForm
    template_name = 'event_form.html'

    def get_success_url(self):
        """Return the home page."""
        return reverse('index')


class EventUpdateView(UpdateView):
    """UpdateView for the Event model."""

    model = Event
    form_class = EventForm
    template_name = 'event_form.html'

    def get_success_url(self):
        """Return the home page."""
        return reverse('index')


class EventDeleteView(DeleteView):
    """DeleteView for the Event model."""

    model = Event
    template_name = 'event_confirm_delete.html'

    def get_success_url(self):
        """Return the home page."""
        return reverse('index')


class EventListView(ListView):
    """ListView for the Event model."""

    model = Event
    template_name = 'index.html'
    context_object_name = 'events'


class VenueListView(ListView):
    """ListView for the Venue model."""

    model = Venue
    template_name = 'venue_list.html'
    context_object_name = 'venues'
