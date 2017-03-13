"""Views for calendar app."""
from django.urls import reverse

from .models import Event
from .forms import EventCreateForm

from django.views.generic import CreateView, DeleteView, DetailView, ListView


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'
    context_object_name = 'event'


class EventCreateView(CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'event_form.html'

    def get_success_url(self):
        return reverse('index')


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'

    def get_success_url(self):
        return reverse('index')


class EventListView(ListView):
    model = Event
    template_name = 'index.html'
    context_object_name = 'events'
