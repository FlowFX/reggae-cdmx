"""reggae_cdmx/views.py."""
import datetime

from braces.views import LoginRequiredMixin

from django.contrib import messages
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
        return NotImplemented  # pragma: no cover

    def form_valid(self, form):
        """Display success message when form validated."""
        messages.success(self.request, self.success_msg)
        return super(FormActionMixin, self).form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     """Add 'Cancel' button redirect."""
    #     if "cancel" in request.POST:
    #         return HttpResponseRedirect(self.get_success_url())
    #     else:
    #         return super(FormActionMixin, self).post(request, *args, **kwargs)


class HomePage(ListView):
    """View for home page."""

    model = Event
    template_name = 'index.html'
    context_object_name = 'events'

    def get_queryset(self):
        """Return all future events."""
        qs = self.model._default_manager
        qs = qs.select_related('venue')
        qs = qs.filter(date__gte=datetime.date.today())
        qs = qs.order_by('date')
        qs = qs.values('slug', 'date', 'title', 'venue__name')

        return qs

    def get_context_data(self, **kwargs):
        """Add to the context."""
        context = super(HomePage, self).get_context_data(**kwargs)
        events = context['events']

        calendar = {}

        for event in events:
            date = event.get('date')
            year = date.year
            month = date.strftime('%B')
            week = date.isocalendar()[1]
            day = date.isocalendar()[2]

            if not calendar.get(year):
                calendar[year] = {
                    'year': year,
                    'months': {},
                }

            if not calendar[year]['months'].get(month):
                calendar[year]['months'][month] = {
                    'month': month,
                    'weeks': {},
                }

            if not calendar[year]['months'][month]['weeks'].get(week):
                calendar[year]['months'][month]['weeks'][week] = {
                    'week': week,
                    'days': {},
                }

            if not calendar[year]['months'][month]['weeks'][week]['days'].get(day):
                calendar[year]['months'][month]['weeks'][week]['days'][day] = {
                    'date': date,
                    'events': [],
                }

            event['url'] = reverse('events:detail', kwargs={'slug': event['slug']})
            calendar[year]['months'][month]['weeks'][week]['days'][day]['events'] += [event]

        context['calendar'] = calendar
        return context


class EventDetailView(DetailView):
    """DetailView for the Event model."""

    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'


class EventCreateView(LoginRequiredMixin, FormActionMixin, CreateView):
    """CreateView for the Event model."""

    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_msg = 'Event created'


class EventUpdateView(LoginRequiredMixin, FormActionMixin, UpdateView):
    """UpdateView for the Event model."""

    model = Event
    form_class = EventForm
    template_name = 'events/event_form.html'
    success_msg = 'Event updated'

    def get_success_url(self):
        """Return the home page."""
        return reverse('events:list')


class EventDeleteView(LoginRequiredMixin, FormActionMixin, DeleteView):
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


class EventListView(LoginRequiredMixin, ListView):
    """ListView for the Event model."""

    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    ordering = '-date'

    def get_queryset(self):
        """Return all events."""
        qs = self.model._default_manager
        qs = qs.select_related('venue')
        qs = qs.order_by('-date')

        return qs
