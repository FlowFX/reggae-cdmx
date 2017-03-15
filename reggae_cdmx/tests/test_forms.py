import pytest

from ..models import Venue
from ..factories import VenueFactory
from ..forms import EventForm

from datetime import date


@pytest.mark.parametrize('title, date, validity', [
    ('Bungalo Dub ft. Jahshua Soundman', date(2017, 8, 20), True),
    ('Bungalo Dub ft. Jahshua Soundman', '20/08/2017', True),
    ('Bungalo Dub', '', False),   # empty date
    ('', '20/08/2017', False),    # empty title
    ])
def test_event_create_form(title, date, validity):
    """Test form validation for EventForm."""
    form = EventForm(data={
        'title': title,
        'date': date,
    })

    assert form.is_valid() is validity



    # event = EventFactory.build()

    # with patch.object(EventUpdateView, 'get_object', return_value=event):