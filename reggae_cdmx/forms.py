"""Forms definitions."""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Event

from django import forms


class EventForm(forms.ModelForm):
    """Form for EventCreateView."""

    class Meta:  # noqa
        model = Event
        fields = (
            'title',
            'date',
            'venue',
        )

    widgets = {
        # 'date': forms.DateInput(format=['%d/%m/%y']),
    }

    def __init__(self, *args, **kwargs):
        """Add Crispy Forms FormHelper."""
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
