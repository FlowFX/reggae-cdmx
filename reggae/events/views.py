"""reggae_cdmx/views.py."""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)

from .forms import EventForm
from .models import Event


class FormActionMixin(object):
    """Custom functionality for data-manipulation views.

    1. display success messages
    2. make the cancel button work
    """

    @property
    def success_msg(self):  # noqa: D102
        return NotImplemented

    def form_valid(self, form):
        """Display success message when form validated."""
        messages.success(self.request, self.success_msg)
        return super(FormActionMixin, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """Add 'Cancel' button redirect."""
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(FormActionMixin, self).post(request, *args, **kwargs)


class IndexView(ListView):
    """View for home page."""

    model = Event
    template_name = 'index.html'
    context_object_name = 'events'


class EventDetailView(DetailView):
    """DetailView for the Event model."""

    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventCreateView(FormActionMixin, CreateView):
    """CreateView for the Event model."""

    model = Event
    form_class = EventForm
    template_name = 'model_form.html'
    success_msg = 'Event created'

    def get_success_url(self):
        """Return the home page."""
        return reverse('events:list')


class EventUpdateView(FormActionMixin, UpdateView):
    """UpdateView for the Event model."""

    model = Event
    form_class = EventForm
    template_name = 'model_form.html'
    success_msg = 'Event updated'

    def get_success_url(self):
        """Return the home page."""
        return reverse('index')


class EventDeleteView(FormActionMixin, DeleteView):
    """DeleteView for the Event model."""

    model = Event
    template_name = 'model_delete.html'
    success_msg = 'Event deleted'

    def get_success_url(self):
        """Return the home page."""
        return reverse('events:list')

    def delete(self, request, *args, **kwargs):
        """Display success message on delete."""
        messages.success(self.request, self.success_msg)
        return super(EventDeleteView, self).delete(request, *args, **kwargs)


class EventListView(ListView):
    """ListView for the Event model."""

    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
