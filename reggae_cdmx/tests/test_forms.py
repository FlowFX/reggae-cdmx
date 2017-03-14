import pytest

from ..forms import EventForm

from datetime import date


@pytest.mark.parametrize('title, venue, date, validity', [
    ('Bungalo Dub ft. Jahshua Soundman', 'Kaliman Bar', date(2017, 8, 20), True),
    ('Bungalo Dub ft. Jahshua Soundman', 'Kaliman Bar', '20/08/2017', True),
    ('Bungalo Dub', 'Kaliman Bar', '', False),   # empty date
    ('', 'Kaliman Bar', '20/08/2017', False),    # empty title
    ('Bungalo Dub ft. Jahshua Soundman', '', '20/08/2017', False),      # empty venue
    ])
def test_event_create_form(title, date, venue, validity):
    """Test form validation for EventForm."""
    form = EventForm(data={
        'title': title,
        'date': date,
        'venue': venue,
    })

    assert form.is_valid() is validity
