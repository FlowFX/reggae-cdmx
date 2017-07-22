"""Forms definitions."""
from django import forms

from .models import Venue


class VenueForm(forms.ModelForm):
    """Form for VenueCreateView."""

    class Meta:  # noqa
        model = Venue
        fields = (
            'name',
        )
