"""Forms definitions."""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Event, Venue

from django.forms import ModelForm


class SubmitButtonsMixin(object):
    """Add submit and cancel buttons to form layout."""

    def __init__(self, *args, **kwargs):
        """Add Crispy Forms FormHelper."""
        super(SubmitButtonsMixin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )


class EventForm(SubmitButtonsMixin, ModelForm):
    """Form for EventCreateView."""

    class Meta:  # noqa
        model = Event
        fields = (
            'title',
            'date',
            'venue',
        )


class VenueForm(SubmitButtonsMixin, ModelForm):
    """Form for VenueCreateView."""

    class Meta:  # noqa
        model = Venue
        fields = (
            'name',
        )
