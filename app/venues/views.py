"""reggae/venues/views.py."""

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView,
                                  DetailView, ListView, UpdateView)

from .forms import VenueForm
from .models import Venue


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


class VenueListView(ListView):
    """ListView for the Venue model."""

    model = Venue
    template_name = 'venues/venue_list.html'
    context_object_name = 'venues'


class VenueDetailView(DetailView):
    """DetailView for the Venue model."""

    model = Venue
    # template_name = 'venue_list.html'
    context_object_name = 'venue'


class VenueCreateView(FormActionMixin, CreateView):
    """CreateView for the Venue model."""

    model = Venue
    form_class = VenueForm
    template_name = 'model_form.html'
    success_msg = 'Venue created'

    def get_success_url(self):
        """Return the venue list."""
        return reverse('venues:list')


class VenueUpdateView(FormActionMixin, UpdateView):
    """UpdateView for the Venue model."""

    model = Venue
    form_class = VenueForm
    template_name = 'model_form.html'
    success_msg = 'Venue updated'

    def get_success_url(self):
        """Return the venue list."""
        return reverse('venues:list')


class VenueDeleteView(FormActionMixin, DeleteView):
    """DeleteView for the Venue model."""

    model = Venue
    template_name = 'model_delete.html'
    success_msg = 'Venue deleted'

    def get_success_url(self):
        """Return the home page."""
        return reverse('venues:list')

    def delete(self, request, *args, **kwargs):
        """Display success message on delete."""
        messages.success(self.request, self.success_msg)
        return super(VenueDeleteView, self).delete(request, *args, **kwargs)
