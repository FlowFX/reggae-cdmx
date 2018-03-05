"""Forms definitions."""
from app.events.models import Event

from django import forms


class EventForm(forms.ModelForm):
    """Form for EventCreateView."""

    class Meta:  # noqa
        model = Event
        fields = (
            'title',
            'date',
            'venue',
            'description',
            'url',
            'flyer_image',
        )
