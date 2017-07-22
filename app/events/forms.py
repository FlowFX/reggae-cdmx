"""Forms definitions."""
from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """Form for EventCreateView."""

    class Meta:  # noqa
        model = Event
        fields = (
            'title',
            'date',
            'venue',
        )
