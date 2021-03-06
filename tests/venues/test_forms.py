"""Unit tests for venues.forms."""
from app.venues import forms

import pytest


@pytest.mark.parametrize(
    'name, validity',
    [('Kaliman Bar', True),
     ('', False),    # empty name
     ])
def test_venue_create_form(name, validity):
    """Test form validation for EventForm."""
    form = forms.VenueForm(data={
        'name': name,
    })

    assert form.is_valid() is validity
