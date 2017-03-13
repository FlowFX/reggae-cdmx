"""Views for calendar app."""

from .models import Event
from .forms import EventCreateForm

from django.views.generic import CreateView, DetailView, ListView


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


class EventCreateView(CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'event_form.html'


class EventListView(ListView):
    model = Event
    template_name = 'index.html'
    context_object_name = 'events'
