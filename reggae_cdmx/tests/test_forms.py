import pytest

from ..forms import EventCreateForm

from datetime import date

@pytest.mark.parametrize(
    'title, date, validity',
    [('Bungalo Dub ft. Jahshua Soundman', date(2017, 8, 20), True),
     ('Bungalo Dub ft. Jahshua Soundman', '20/08/2017', True),
     ('Bungalo Dub', '', False),
     ])
def test_event_create_form(title, date, validity):
    """Test form validation for RentForm."""
    form = EventCreateForm(data={
        'title': title,
        'date': date,
    })

    assert form.is_valid() is validity