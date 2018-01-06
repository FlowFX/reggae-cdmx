"""Unit tests for form validation."""
from datetime import date

from app.events.forms import EventForm

import pytest


@pytest.mark.parametrize(
    'title, date, venue, valid_a',
    [('Bungalo Dub ft. Jahshua Soundman', date(2017, 8, 20), None, True),
     ('Bungalo Dub', '', None, False),   # empty date
     ('', '20/08/2017', None, False),    # empty title
     ])
@pytest.mark.parametrize(
    'description, valid_b',
    [('A description', True),
     ('', True),   # empty description
     ])
@pytest.mark.parametrize(
    'fb_event_url, valid_c',
    [('https://www.facebook.com/events/2001223273532037/', True),
     ('https://www.fakebook.com/events/2001223273532037/', False),  # typo
     ('', True),   # empty event url
     ])
def test_event_form(title, date, venue, description, fb_event_url, valid_a, valid_b, valid_c):
    """Test form validation for EventForm."""
    form = EventForm(data={
        'title': title,
        'date': date,
        'venue': venue,
        'description': description,
        'fb_event_url': fb_event_url,
    })

    assert form.is_valid() is (valid_a and valid_b and valid_c)
