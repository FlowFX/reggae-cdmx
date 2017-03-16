"""Forms definitions."""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Event, Venue

from django import forms


# class SubmitButtonsMixin(object):

#     def post(self, request, *args, **kwargs):
#         """Add 'Cancel' button redirect."""
#         if "cancel" in request.POST:
#             url = reverse('index')     # or e.g. reverse(self.get_success_url())
#             return HttpResponseRedirect(url)
#         else:
#         return 
#         super(FormActionMixin, self).post(request, *args, **kwargs)


class EventForm(forms.ModelForm):
    """Form for EventCreateView."""

    class Meta:  # noqa
        model = Event
        fields = (
            'title',
            'date',
            'venue',
        )

    # widgets = {
    #     'date': forms.DateInput(format=['%d/%m/%y']),
    # }

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


class VenueForm(forms.ModelForm):
    """Form for VenueCreateView."""

    class Meta:  # noqa
        model = Venue
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        """Add Crispy Forms FormHelper."""
        super(VenueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'Submit'))
        self.helper.add_input(Submit(
            'cancel',
            'Cancel',
            css_class='btn-danger',
            formnovalidate='formnovalidate',
            )
        )
