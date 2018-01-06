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
            'fb_event_url',
            'flyer_image',
        )

    def clean_fb_event_url(self):
        """Check for valid Facebook event URLs."""
        url = self.cleaned_data['fb_event_url']

        # heuristics to check validity of a facebook event url
        fb_event_content = ['facebook', 'events']

        if url:
            for x in fb_event_content:
                if x not in url:
                    raise forms.ValidationError('Not a Facebook Event URL')

        return url
