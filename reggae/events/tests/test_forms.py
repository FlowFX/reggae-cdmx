"""Unit tests for form validation."""
from datetime import date

import pytest

from reggae.events.forms import EventForm


@pytest.mark.parametrize('title, date, venue, validity', [
    ('Bungalo Dub ft. Jahshua Soundman', date(2017, 8, 20), None, True),
    ('Bungalo Dub ft. Jahshua Soundman', '20/08/2017', None, True),
    ('Bungalo Dub', '', None, False),   # empty date
    ('', '20/08/2017', None, False),    # empty title
    ])
def test_event_create_form(title, date, venue, validity):
    """Test form validation for EventForm."""
    form = EventForm(data={
        'title': title,
        'date': date,
        'venue': venue,
    })

    assert form.is_valid() is validity
