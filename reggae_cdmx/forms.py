
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Event

from django import forms


class EventCreateForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'title',
            'date',
        )

    widgets = {
        # 'date': forms.DateInput(format=['%d/%m/%y']),
    }

    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
